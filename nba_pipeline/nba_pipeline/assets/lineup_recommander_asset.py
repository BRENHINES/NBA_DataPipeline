import polars as pl
from pathlib import Path
from nba_pipeline.nba_pipeline.models.features.team_stats_features import build_team_profiles
from dagster import asset
from nba_pipeline.nba_pipeline.models.team_lineup_recommander import recommend_lineup_against

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data/processed"

@asset(required_resource_keys={"db"}, deps=[
    "player_stats_by_season",
    "available_teams"
])
def recommend_optimal_lineup():
    # Charger les données d'équipes disponibles
    team_profiles = build_team_profiles()

    # Identifier toutes les combinaisons d'équipes adversaires vs notre équipe (par saison)
    all_lineups = []
    seasons = team_profiles.select("season").unique().to_series().to_list()
    teams = team_profiles.select("team_id").unique().to_series().to_list()

    for season in seasons:
        for our_team_id in teams:
            for adversary_team_id in teams:
                if adversary_team_id != our_team_id:
                    try:
                        lineup = recommend_lineup_against(
                            adversary_team_id=adversary_team_id,
                            season=season,
                            our_team_id=our_team_id
                        ).with_columns([
                            pl.lit(season).alias("season"),
                            pl.lit(our_team_id).alias("team_id"),
                            pl.lit(adversary_team_id).alias("opponent_team_id")
                        ])
                        all_lineups.append(lineup)
                    except Exception as e:
                        print(f"Échec lineup {season} {our_team_id} vs {adversary_team_id}: {e}")

    if all_lineups:
        return pl.concat(all_lineups)
    else:
        return pl.DataFrame()
