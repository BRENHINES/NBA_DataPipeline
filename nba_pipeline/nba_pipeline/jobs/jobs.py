from dagster import define_asset_job

# Extraction uniquement
extraction_job = define_asset_job(
    name="extraction_job",
    selection=[
        "available_seasons",
        "available_teams",
        "players_by_season",
        "games_by_season",
        "player_stats_by_season",
        "draft_by_season"
    ]
)

# Sauvegarde des données (backup)
backup_job = define_asset_job(
    name="backup_job",
    selection=["export_backups_to_parquet", "export_enriched_player_stats"]
)

# Tranform et enrichissement des données
transform_job = define_asset_job(
    name="transform_job",
    selection=[
        "enrich_player_stats_with_kpis",
        "export_enriched_player_stats"
    ]
)

# ETL complet
full_etl_job = define_asset_job(
    name="full_etl_job",
    selection=[
        "available_seasons",
        "available_teams",
        "players_by_season",
        "games_by_season",
        "player_stats_by_season",
        "draft_by_season",
        "enrich_player_stats_with_kpis",
        "export_backups_to_parquet",
        "export_enriched_player_stats",
    ]
)

predict_draft_flops_job = define_asset_job(
    name="predict_draft_flops_job",
    selection=["predict_draft_flops"]
)

predict_playoffs_winners_job = define_asset_job(
    name="predict_playoffs_winners_job",
    selection=["predict_playoffs_winners"]
)

recommend_optimal_lineup_job = define_asset_job(
    name="recommend_optimal_lineup_job",
    selection=["recommend_optimal_lineup"]
)
