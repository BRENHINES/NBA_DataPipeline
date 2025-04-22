import polars as pl
from pathlib import Path
from sklearn.cluster import KMeans
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data/processed"


def build_team_profiles(n_clusters=4):
    stats_df = pl.read_parquet(DATA_DIR / "nba_player_stats.parquet")

    # Regrouper les performances par match et par équipe
    team_game_stats = (
        stats_df.group_by(["season", "team_id", "game_id"]).agg([
            pl.col("points").mean().alias("pts"),
            pl.col("totReb").mean().alias("reb"),
            pl.col("assists").mean().alias("ast"),
            pl.col("efficiency_score").mean().alias("eff"),
        ])
    )

    # Calculer les moyennes globales par équipe sur la saison
    team_profiles = (
        team_game_stats.group_by(["season", "team_id"]).agg([
            pl.col("pts").mean().alias("avg_pts"),
            pl.col("reb").mean().alias("avg_reb"),
            pl.col("ast").mean().alias("avg_ast"),
            pl.col("eff").mean().alias("avg_eff"),
        ])
    )

    # Clustering avec sklearn
    profile_np = team_profiles.select(["avg_pts", "avg_reb", "avg_ast", "avg_eff"]).to_numpy()
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(profile_np)

    # Ajout du cluster dans Polars
    team_profiles = team_profiles.with_columns([
        pl.Series(name="team_profile", values=labels)
    ])

    return team_profiles
