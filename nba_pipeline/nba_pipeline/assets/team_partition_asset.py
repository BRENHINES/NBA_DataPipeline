from dagster import asset
from nba_pipeline.nba_pipeline.resources.db_ressources import PostgresResource

@asset(required_resource_keys={"db"})
def team_partition_hierarchy(context):
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT conference, division, name
        FROM nba_teams
        ORDER BY conference, division, name;
    """)

    rows = cursor.fetchall()
    hierarchy = {}

    for conf, div, name in rows:
        if conf not in hierarchy:
            hierarchy[conf] = {}
        if div not in hierarchy[conf]:
            hierarchy[conf][div] = []
        hierarchy[conf][div].append(name)

    cursor.close()
    conn.close()

    context.log.info(f"Hiérarchie équipes : {hierarchy}")
    return hierarchy
