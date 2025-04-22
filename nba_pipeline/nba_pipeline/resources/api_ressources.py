from dagster import ConfigurableResource
from ..src.nba_client import NBAClient

class NBAAPIResource(ConfigurableResource):
    api_key: str = "4f700f64c4msh19516836b98fea8p19547djsn9dcf8f30ec7d"
    host: str = "api-nba-v1.p.rapidapi.com"

    def get_client(self) -> NBAClient:
        return NBAClient(api_key=self.api_key, host=self.host)
