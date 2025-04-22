import polars as pl
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # Sortir de features/ → models/ → nba_pipeline/
DATA_DIR = BASE_DIR / "data"

def build_draft_dataset(
        draft_path=DATA_DIR / "raw/nba_drafts.parquet",
        stats_path=DATA_DIR / "processed/nba_player_stats.parquet"
):
    # Charger les données
    df_draft = pl.read_parquet(Path(draft_path))
    df_stats = pl.read_parquet(Path(stats_path))

    # Agréger les stats des joueurs draftés par saison
    df_stats_summary = (
        df_stats
        .group_by(["player_id", "season"])
        .agg([
            pl.col("points").mean().alias("avg_points"),
            pl.col("assists").mean().alias("avg_assists"),
            pl.col("totReb").mean().alias("avg_rebounds"),
            pl.col("efficiency_score").mean().alias("avg_efficiency"),
            pl.col("minutes_played").mean().alias("avg_minutes")
        ])
    )

    # Fusion avec les drafts
    df_joined = df_draft.join(
        df_stats_summary,
        left_on=["player_id", "season"],
        right_on=["player_id", "season"],
        how="left"
    )

    # Créer une colonne binaire "is_flop"
    # (simple critère de base : moins de 10 points et 20 min par match en moyenne)
    df_final = df_joined.with_columns([
        (
            (pl.col("avg_points") < 10) &
            (pl.col("avg_minutes") < 20)
        ).cast(pl.Int8).alias("is_flop")
    ])

    return df_final
