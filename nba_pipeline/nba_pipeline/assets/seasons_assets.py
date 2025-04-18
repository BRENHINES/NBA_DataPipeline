from dagster import asset
from nba_pipeline.nba_pipeline.resources.api_ressources import NBAAPIResource

@asset(required_resource_keys={"nba_api"})
def available_seasons(context) -> list:
    client = context.resources.nba_api.get_client()
    seasons = client.get_seasons()
    context.log.info(f"Saisons récupérées : {seasons}")
    return seasons
