from dagster import asset
from pathlib import Path
import polars as pl

@asset(required_resource_keys={"db"}, deps=[
    "available_seasons", "available_teams", "players_by_season",
    "games_by_season", "player_stats_by_season", "draft_by_season"
])
def export_backups_to_parquet(context):
    output_dir_raw = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
    output_dir_raw.mkdir(parents=True, exist_ok=True)
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    table_names = [
        "nba_seasons",
        "nba_teams",
        "nba_players",
        "nba_games",
        "nba_player_stats",
        "nba_drafts"
    ]

    for table in table_names:
        context.log.info(f"Export {table}...")
        df = pl.read_database(f"SELECT * FROM {table}", conn)
        path = output_dir_raw / f"{table}.parquet"
        df.write_parquet(str(path))
        context.log.info(f"{table} exporté vers {path}")

    cursor.close()
    conn.close()


@asset(
    required_resource_keys={"db"},
    deps=["enrich_player_stats_with_kpis"]
)
def export_enriched_player_stats(context):
    conn = context.resources.db.get_connection()
    output_dir_processed = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
    output_dir_processed.mkdir(parents=True, exist_ok=True)
    path = output_dir_processed / "nba_player_stats.parquet"

    df = pl.read_database("SELECT * FROM nba_player_stats", conn)
    df.write_parquet(path)

    context.log.info(f"Statistiques enrichies exportées vers {path}")
    return path.as_posix()
