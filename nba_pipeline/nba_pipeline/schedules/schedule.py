from dagster import ScheduleDefinition
from nba_pipeline.nba_pipeline.jobs import extract_job

daily_schedule = ScheduleDefinition(
    job=extract_job,
    cron_schedule="0 6 * * *",  # Tous les jours à 6h du matin UTC
    name="daily_seasons_schedule"
)
