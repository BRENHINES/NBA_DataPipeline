import polars as pl
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data/processed"
RAW_DIR = BASE_DIR / "data/raw"

def build_playoffs_dataset():
    games_df = pl.read_parquet(RAW_DIR / "nba_games.parquet")
    stats_df = pl.read_parquet(DATA_DIR / "nba_player_stats.parquet")

    # Filtrer les matchs de playoffs uniquement
    playoff_games = games_df.filter(pl.col("type") == "Playoffs")

    # Moyennes des performances par joueur et par match
    team_avg_stats = (
        stats_df.group_by(["game_id", "team_id"]).agg([
            pl.col("points").mean().alias("team_avg_points"),
            pl.col("assists").mean().alias("team_avg_assists"),
            pl.col("totReb").mean().alias("team_avg_rebounds"),
            pl.col("efficiency_score").mean().alias("team_efficiency")
        ])
    )

    # Fusionner les données équipe domicile
    home_df = (
        playoff_games.join(team_avg_stats, left_on=["id", "home_team_id"], right_on=["game_id", "team_id"], how="inner")
        .rename({
            "team_avg_points": "home_points_avg",
            "team_avg_assists": "home_assists_avg",
            "team_avg_rebounds": "home_reb_avg",
            "team_efficiency": "home_eff"
        })
    )

    # Fusionner les données équipe visiteuse
    full_df = (
        home_df.join(team_avg_stats, left_on=["id", "away_team_id"], right_on=["game_id", "team_id"], how="inner")
        .rename({
            "team_avg_points": "away_points_avg",
            "team_avg_assists": "away_assists_avg",
            "team_avg_rebounds": "away_reb_avg",
            "team_efficiency": "away_eff"
        })
    )

    # Label : 1 si l'équipe à domicile gagne, sinon 0
    full_df = full_df.with_columns([
        (pl.col("home_score") > pl.col("away_score")).cast(pl.Int8).alias("home_win")
    ])

    return full_df.select([
        "home_team_id", "away_team_id", "home_points_avg", "home_assists_avg", "home_reb_avg", "home_eff",
        "away_points_avg", "away_assists_avg", "away_reb_avg", "away_eff", "home_win"
    ])