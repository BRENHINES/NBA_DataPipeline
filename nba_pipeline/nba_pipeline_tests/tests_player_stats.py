import polars as pl
from pathlib import Path

def test_player_stats_columns():
    df = pl.read_parquet(Path("data/processed/nba_player_stats.parquet"))

    expected_columns = {
        "player_id", "game_id", "team_id", "season", "points",
        "minutes_played", "fgp", "efficiency_score"
    }

    assert expected_columns.issubset(set(df.columns)), "Colonnes manquantes dans stats"

def test_efficiency_score_non_negative():
    df = pl.read_parquet(Path("data/processed/nba_player_stats.parquet"))
    assert df["efficiency_score"].min() >= 0, "Valeur d'efficacité négative"

def test_minutes_played_positive():
    df = pl.read_parquet(Path("data/processed/nba_player_stats.parquet"))
    assert df["minutes_played"].mean() > 0, "Minutes moyennes incorrectes"
