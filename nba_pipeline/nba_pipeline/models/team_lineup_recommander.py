import polars as pl
from pathlib import Path
from nba_pipeline.nba_pipeline.models.features.team_stats_features import build_team_profiles

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data/processed"


def recommend_lineup_against(adversary_team_id: int, season: str, our_team_id: int, top_k=5):
    # Charger les profils d'équipes
    team_profiles = build_team_profiles()

    # Identifier le profil de l'adversaire
    adversary_profile = (
        team_profiles.filter((pl.col("team_id") == adversary_team_id) & (pl.col("season") == season))
        .select("team_profile")
        .to_series()
        .to_list()[0]
    )

    # Charger les stats des joueurs
    stats_df = pl.read_parquet(DATA_DIR / "nba_player_stats.parquet")

    # Fusionner avec le profil des adversaires affrontés
    enriched_df = stats_df.join(
        team_profiles.select(["team_id", "season", "team_profile"]),
        left_on=["opponent_team_id", "season"],
        right_on=["team_id", "season"],
        how="inner"
    )

    # Filtrer : nos joueurs contre des équipes du même profil que l'adversaire
    matchup_df = enriched_df.filter(
        (pl.col("team_id") == our_team_id) &
        (pl.col("team_profile") == adversary_profile) &
        (pl.col("season") == season)
    )

    # Moyenne par joueur contre ce type d'équipe
    player_scores = matchup_df.group_by("player_id").agg([
        pl.col("efficiency_score").mean().alias("avg_efficiency_vs_profile"),
        pl.col("points").mean().alias("avg_pts_vs_profile"),
        pl.col("minutes_played").mean().alias("avg_min")
    ])

    # Trier par efficacité et minutes jouées (fiabilité)
    best_lineup = player_scores.sort([
        pl.col("avg_efficiency_vs_profile").desc(),
        pl.col("avg_min").desc()
    ]).head(top_k)

    return best_lineup
