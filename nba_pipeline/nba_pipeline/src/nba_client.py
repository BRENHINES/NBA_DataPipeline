import requests
import os

class NBAClient:
    def __init__(self, api_key: str = None, host: str = None):
        self.api_key = api_key or os.getenv("NBA_API_KEY")
        self.host = host or os.getenv("NBA_API_HOST", "api-nba-v1.p.rapidapi.com")
        self.base_url = f"https://{self.host}"

        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }

    def get_seasons(self):
        url = f"{self.base_url}/seasons"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("response", [])
