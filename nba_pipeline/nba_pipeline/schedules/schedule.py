from dagster import ScheduleDefinition
from nba_pipeline.nba_pipeline.jobs.jobs import extraction_job, backup_job, full_etl_job

# Draft annuelle en août (UTC)
annual_draft_schedule = ScheduleDefinition(
    job_name="full_etl_job",
    cron_schedule="0 4 1 8 *",  # 1er août à 4h du matin UTC
    execution_timezone="UTC",
    name="annual_draft_schedule",
    tags={"dagster_partition": "2024"},
    run_config={"ops": {"draft_by_season": {}}}
)

# Joueurs, saisons, backups annuels
annual_season_backup_schedule = ScheduleDefinition(
    job_name="full_etl_job",
    cron_schedule="30 4 1 8 *",  # 1er août à 4h30 UTC
    execution_timezone="UTC",
    name="annual_season_backup_schedule",
    tags={"dagster_partition": "2024"},
    run_config={"ops": {
        "available_seasons": {},
        "players_by_season": {},
        "export_backups_to_parquet": {}
    }}
)

# Matchs & stats chaque jour à 6h
daily_game_stat_schedule = ScheduleDefinition(
    job_name="extraction_job",
    cron_schedule="0 6 * 10-12,1-6 *",  # Tous les jours à 6h d'octobre à juin
    execution_timezone="UTC",
    name="daily_game_stat_schedule",
    tags={"dagster_partition": "latest"},
    run_config={"ops": {
        "games_by_season": {},
        "player_stats_by_season": {}
    }}
)

ml_flop_prediction_schedule = ScheduleDefinition(
    job_name="predict_draft_flops_job",
    cron_schedule="0 6 1 8 *",  # Chaque 1er août à 2h
    execution_timezone="UTC",
    name="ml_flop_prediction_schedule"
)

playoffs_model_schedule = ScheduleDefinition(
    job_name="predict_playoffs_winners_job",
    cron_schedule="0 3 10 4 *",  # 10 avril à 3h UTC (début habituel des playoffs)
    execution_timezone="UTC",
    name="playoffs_model_schedule"
)
