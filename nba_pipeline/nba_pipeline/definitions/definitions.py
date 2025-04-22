from nba_pipeline.nba_pipeline import assets
from dagster import Definitions, load_assets_from_modules
from nba_pipeline.nba_pipeline.partitions.season_partitions import season_partition_def
from nba_pipeline.nba_pipeline.sensors.sensors import match_day_sensor
from nba_pipeline.nba_pipeline.resources.api_ressources import NBAAPIResource
from nba_pipeline.nba_pipeline.resources.db_ressources import PostgresResource
from nba_pipeline.nba_pipeline.jobs.jobs import extraction_job, backup_job, full_etl_job, transform_job, predict_draft_flops_job, predict_playoffs_winners_job, recommend_optimal_lineup_job
from nba_pipeline.nba_pipeline.schedules.schedule import annual_draft_schedule, annual_season_backup_schedule, daily_game_stat_schedule, ml_flop_prediction_schedule, playoffs_model_schedule

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[
        extraction_job,
        backup_job,
        full_etl_job,
        transform_job,
        predict_draft_flops_job,
        predict_playoffs_winners_job,
        recommend_optimal_lineup_job
    ],
    schedules=[
        annual_draft_schedule,
        annual_season_backup_schedule,
        daily_game_stat_schedule,
        ml_flop_prediction_schedule,
        playoffs_model_schedule
    ],
    sensors=[match_day_sensor],
    resources={
        "nba_api": NBAAPIResource(api_key="4f700f64c4msh19516836b98fea8p19547djsn9dcf8f30ec7d"),
        "db": PostgresResource(
            host="localhost",
            port=5432,
            user="nbauser",
            password="nbapass",
            dbname="nba_base"
        )
    }
)
