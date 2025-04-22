from dagster import asset
from nba_pipeline.nba_pipeline.partitions.season_partitions import season_partition_def

@asset(
    partitions_def=season_partition_def,
    required_resource_keys={"nba_api", "db"},
    deps=["available_seasons"]
)
def draft_by_season(context):
    season = context.partition_key
    client = context.resources.nba_api.get_client()
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    context.log.info(f"Extraction de la draft pour la saison {season}")
    players = client.get_players(season=season)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nba_drafts (
            player_id INT PRIMARY KEY,
            season TEXT,
            round TEXT,
            pick TEXT,
            team_id INT,
            team_name TEXT,
            firstname TEXT,
            lastname TEXT,
            position TEXT,
            country TEXT,
            birth_date TEXT,
            college TEXT
        );
    """)

    for p in players:
        draft = p.get("draft", {})
        draft_team = draft.get("team", {})

        if not draft:
            continue

        cursor.execute("""
            INSERT INTO nba_drafts (
                player_id, season, round, pick, team_id,
                firstname, lastname, position, country,
                birth_date, college
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (player_id) DO NOTHING;
        """, (
            p["id"],
            season,
            draft.get("round"),
            draft.get("pick"),
            draft_team.get("id"),
            draft_team.get("name"),
            p["firstname"],
            p["lastname"],
            p.get("leagues", {}).get("standard", {}).get("pos"),
            p.get("birth", {}).get("country"),
            p.get("birth", {}).get("date"),
            p.get("college")
        ))

    conn.commit()
    cursor.close()
    conn.close()

    return players
