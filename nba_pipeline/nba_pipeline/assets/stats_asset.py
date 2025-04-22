from dagster import asset
from nba_pipeline.nba_pipeline.partitions.season_partitions import season_partition_def


def parse_minutes(min_str):
    try:
        min_part, sec_part = map(int, min_str.split(":"))
        return round(min_part + sec_part / 60, 2)
    except:
        return 0.0

def parse_percent(value):
    try:
        return float(value.replace("%", ""))
    except:
        return 0.0

def parse_plus_minus(value):
    try:
        return float(value)
    except:
        return 0.0


@asset(
    partitions_def=season_partition_def,
    required_resource_keys={"nba_api", "db"},
    deps=["players_by_season", "games_by_season"]
)
def player_stats_by_season(context):
    season = context.partition_key
    client = context.resources.nba_api.get_client()
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    # Récupération des matchs enregistrés en base
    cursor.execute("SELECT id FROM nba_games WHERE season = %s;", (season,))
    match_ids = [row[0] for row in cursor.fetchall()]
    context.log.info(f"{len(match_ids)} matchs à traiter pour la saison {season}")

    # Création table si besoin
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nba_player_stats (
            player_id INT,
            game_id INT,
            team_id INT,
            pos TEXT,
            min TEXT,
            points INT,
            fgm INT,
            fga INT,
            fgp TEXT,
            ftm INT,
            fta INT,
            ftp TEXT,
            tpm INT,
            tpa INT,
            tpp TEXT,
            offReb INT,
            defReb INT,
            totReb INT,
            assists INT,
            pFouls INT,
            steals INT,
            turnovers INT,
            blocks INT,
            plusMinus TEXT,
            comment TEXT,
            PRIMARY KEY (player_id, game_id)
        );
    """)

    for game_id in match_ids:
        stats = client.get_stats_by_game(game_id)
        for s in stats:
            cursor.execute("""
                INSERT INTO nba_player_stats (
                    player_id, game_id, team_id, pos, min, points,
                    fgm, fga, fgp, ftm, fta, ftp,
                    tpm, tpa, tpp,
                    offReb, defReb, totReb,
                    assists, pFouls, steals, turnovers, blocks,
                    plusMinus, comment
                ) VALUES (%s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s,
                          %s, %s, %s,
                          %s, %s, %s,
                          %s, %s, %s, %s, %s,
                          %s, %s)
                ON CONFLICT (player_id, game_id) DO NOTHING;
            """, (
                s["player"]["id"],
                game_id,
                s["team"]["id"],
                s.get("pos"),
                parse_minutes(s.get("min", "0:00")),
                s.get("points", 0),
                s.get("fgm", 0),
                s.get("fga", 0),
                parse_percent(s.get("fgp", "0")),
                s.get("ftm", 0),
                s.get("fta", 0),
                parse_percent(s.get("ftp", "0")),
                s.get("tpm", 0),
                s.get("tpa", 0),
                parse_percent(s.get("tpp", "0")),
                s.get("offReb", 0),
                s.get("defReb", 0),
                s.get("totReb", 0),
                s.get("assists", 0),
                s.get("pFouls", 0),
                s.get("steals", 0),
                s.get("turnovers", 0),
                s.get("blocks", 0),
                parse_plus_minus(s.get("plusMinus"))
            ))

    conn.commit()
    cursor.close()
    conn.close()
