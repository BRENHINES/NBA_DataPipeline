from dagster import asset
from nba_pipeline.nba_pipeline.partitions.season_partitions import season_partition_def

@asset(required_resource_keys={"nba_api", "db"})
def available_teams(context):
    client = context.resources.nba_api.get_client()
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    teams = client.get_teams()
    context.log.info(f"{len(teams)} équipes récupérées.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nba_teams (
            id INT PRIMARY KEY,
            name TEXT,
            nickname TEXT,
            code TEXT,
            city TEXT,
            logo TEXT,
            conference TEXT,
            division TEXT
        );
    """)

    for t in teams:
        league_info = t.get("leagues", {}).get("standard", {})
        conference = league_info.get("conference")
        division = league_info.get("division")

        cursor.execute("""
            INSERT INTO nba_teams (id, name, nickname, code, city, logo, conference, division)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            t["id"],
            t["name"],
            t["nickname"],
            t["code"],
            t["city"],
            t["logo"],
            conference,
            division
        ))

    conn.commit()
    cursor.close()
    conn.close()

    return teams
