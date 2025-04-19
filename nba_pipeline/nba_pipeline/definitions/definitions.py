from dagster import Definitions, load_assets_from_modules
from nba_pipeline.nba_pipeline import assets
from nba_pipeline.nba_pipeline.jobs import jobs
from nba_pipeline.nba_pipeline.resources.db_ressources import PostgresResource
from nba_pipeline.nba_pipeline.schedules import schedule
from nba_pipeline.nba_pipeline.sensors import sensors
from nba_pipeline.nba_pipeline.resources.api_ressources import NBAAPIResource
from nba_pipeline.nba_pipeline.partitions.season_partitions import season_partitions_def

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[jobs],
    schedules=[schedule],
    sensors=[sensors],
    resources={
        "nba_api": NBAAPIResource(api_key="env:NBA_API_KEY"),
        "db": PostgresResource(
            host="env:DB_HOST",
            port="env:DB_PORT",
            user="env:DB_USER",
            password="env:DB_PASSWORD",
            dbname="env:DB_NAME"
        )
    },
    dynamic_partitions={
            "nba_seasons": season_partitions_def
    }
)
