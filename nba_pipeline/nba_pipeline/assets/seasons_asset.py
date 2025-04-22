from dagster import asset


@asset(required_resource_keys={"nba_api", "db"})
def available_seasons(context) -> list:
    client = context.resources.nba_api.get_client()
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    seasons = client.get_seasons()
    context.log.info(f"Saisons récupérées : {seasons}")

    # Création de la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nba_seasons (
            season VARCHAR PRIMARY KEY
        );
    """)

    # Insertion avec déduplication simple
    for season in seasons:
        cursor.execute(
            "INSERT INTO nba_seasons (season) VALUES (%s) ON CONFLICT DO NOTHING;",
            (season,)
        )
        context.instance.add_dynamic_partitions("nba_teams_partition", [str(season)])

    conn.commit()
    cursor.close()
    conn.close()

    return seasons
