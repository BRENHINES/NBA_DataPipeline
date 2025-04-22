from dagster import asset
import polars as pl

@asset(
    required_resource_keys={"db"},
    deps=["player_stats_by_season"]
)
def enrich_player_stats_with_kpis(context):
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    # Charger les stats brutes
    df = pl.read_database("SELECT * FROM nba_player_stats", conn)

    # Calculs des KPIs
    df = df.with_columns([
        ((pl.col("fgm") + pl.col("tpm")) / pl.when(pl.col("fga") > 0).then(pl.col("fga")).otherwise(1)).alias("efficiency_score"),
        (pl.col("assists") + pl.col("steals") + pl.col("blocks") - pl.col("turnovers")).alias("impact_score"),
        ((pl.col("points") + pl.col("totReb") + pl.col("assists")) / pl.when(pl.col("minutes_played") > 0).then(pl.col("minutes_played")).otherwise(1)).alias("per_minute_score")
    ])

    # Ajout des colonnes dans la base si nécessaire
    cursor.execute("""
        ALTER TABLE nba_player_stats
        ADD COLUMN IF NOT EXISTS efficiency_score FLOAT,
        ADD COLUMN IF NOT EXISTS impact_score FLOAT,
        ADD COLUMN IF NOT EXISTS per_minute_score FLOAT;
    """)

    # Mise à jour des lignes
    for row in df.select(["player_id", "game_id", "efficiency_score", "impact_score", "per_minute_score"]).iter_rows(named=True):
        cursor.execute("""
            UPDATE nba_player_stats
            SET
              efficiency_score = %s,
              impact_score = %s,
              per_minute_score = %s
            WHERE player_id = %s AND game_id = %s;
        """, (
            row["efficiency_score"],
            row["impact_score"],
            row["per_minute_score"],
            row["player_id"],
            row["game_id"]
        ))

    conn.commit()
    cursor.close()
    conn.close()

    context.log.info("KPIs intégrés dans nba_player_stats.")
    return df
