from dagster import asset
from nba_pipeline.nba_pipeline.partitions.season_partitions import season_partition_def


@asset(
    partitions_def=season_partition_def,
    required_resource_keys={"nba_api", "db"},
    deps=["available_seasons"]
)
def games_by_season(context):
    season = context.partition_key
    client = context.resources.nba_api.get_client()
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    context.log.info(f"Extraction des matchs pour la saison {season}")

    # Regular + Playoffs
    regular_games = client.get_games(season=season, game_type="Regular Season")
    playoff_games = client.get_games(season=season, game_type="Playoffs")
    all_games = regular_games + playoff_games

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nba_games (
            id INT PRIMARY KEY,
            season TEXT,
            date_start TEXT,
            date_end TEXT,
            duration TEXT,
            stage INT,
            status_short INT,
            status_long TEXT,
            home_team_id INT,
            away_team_id INT,
            home_team_name TEXT,
            away_team_name TEXT,
            home_score INT,
            away_score INT,
            home_q1 INT,
            home_q2 INT,
            home_q3 INT,
            home_q4 INT,
            away_q1 INT,
            away_q2 INT,
            away_q3 INT,
            away_q4 INT,
            arena_name TEXT,
            arena_city TEXT,
            arena_state TEXT,
            arena_country TEXT,
            times_tied INT,
            lead_changes INT,
            officials TEXT,
            is_playoff BOOLEAN
        );
    """)

    for game in all_games:
        scores_home = game["scores"]["home"]
        scores_away = game["scores"]["visitors"]
        linescore_home = scores_home.get("linescore", ["0"] * 4)
        linescore_away = scores_away.get("linescore", ["0"] * 4)
        arena = game.get("arena", {})
        officials = ", ".join(game.get("officials", []))
        game_type = game.get("games", {}).get("type", "").lower()
        is_playoff = game_type == "playoffs"

        cursor.execute("""
                    INSERT INTO nba_games (
                        id, season, date_start, date_end, duration,
                        stage, status_short, status_long,
                        home_team_id, away_team_id, home_team_name, away_team_name,
                        home_score, away_score,
                        home_q1, home_q2, home_q3, home_q4,
                        away_q1, away_q2, away_q3, away_q4,
                        arena_name, arena_city, arena_state, arena_country,
                        times_tied, lead_changes, officials
                    ) VALUES (%s, %s, %s, %s, %s,
                              %s, %s, %s,
                              %s, %s, %s, %s,
                              %s, %s,
                              %s, %s, %s, %s,
                              %s, %s, %s, %s,
                              %s, %s, %s, %s,
                              %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (
            game["id"],
            season,
            game["date"]["start"],
            game["date"]["end"],
            game["date"].get("duration", ""),
            game.get("stage"),
            game["status"].get("short"),
            game["status"].get("long"),
            game["teams"]["home"]["id"],
            game["teams"]["visitors"]["id"],
            game["teams"]["home"]["name"],
            game["teams"]["visitors"]["name"],
            scores_home.get("points", 0),
            scores_away.get("points", 0),
            int(linescore_home[0]),
            int(linescore_home[1]),
            int(linescore_home[2]),
            int(linescore_home[3]),
            int(linescore_away[0]),
            int(linescore_away[1]),
            int(linescore_away[2]),
            int(linescore_away[3]),
            arena.get("name"),
            arena.get("city"),
            arena.get("state"),
            arena.get("country"),
            game.get("timesTied", 0),
            game.get("leadChanges", 0),
            officials,
            is_playoff
        ))

    conn.commit()
    cursor.close()
    conn.close()
    return all_games
