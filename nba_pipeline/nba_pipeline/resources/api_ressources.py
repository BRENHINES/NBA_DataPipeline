from dagster import ConfigurableResource
from ..src.nba_client import NBAClient

class NBAAPIResource(ConfigurableResource):
    api_key: str
    host: str = "api-nba-v1.p.rapidapi.com"

    def get_client(self) -> NBAClient:
        return NBAClient(api_key=self.api_key, host=self.host)
