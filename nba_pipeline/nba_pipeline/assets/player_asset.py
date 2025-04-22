from dagster import asset
from nba_pipeline.nba_pipeline.partitions.season_partitions import season_partition_def

@asset(
    partitions_def=season_partition_def,
    required_resource_keys={"nba_api", "db"},
    deps=["available_seasons"]
)
def players_by_season(context):
    season = context.partition_key
    client = context.resources.nba_api.get_client()
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    context.log.info(f"Extraction des joueurs pour la saison {season}")
    players = client.get_players(season=season)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nba_players (
            id INT,
            firstname TEXT,
            lastname TEXT,
            team_id INT,
            position TEXT,
            height TEXT,
            weight TEXT,
            birth_date TEXT,
            college TEXT,
            country TEXT,
            nba_start TEXT,
            season TEXT,
            PRIMARY KEY (id, season)
        );
    """)

    for p in players:
        info = p.get("leagues", {}).get("standard", {})
        cursor.execute("""
            INSERT INTO nba_players (
                id, firstname, lastname, team_id, position,
                height, weight, birth_date, college, country,
                nba_start, season
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id, season) DO NOTHING;
        """, (
            p["id"],
            p["firstname"],
            p["lastname"],
            info.get("team", {}).get("id"),
            info.get("pos"),
            info.get("height"),
            info.get("weight"),
            p.get("birth", {}).get("date"),
            p.get("college"),
            p.get("birth", {}).get("country"),
            p.get("nba", {}).get("start"),
            season
        ))

    conn.commit()
    cursor.close()
    conn.close()
    return players
