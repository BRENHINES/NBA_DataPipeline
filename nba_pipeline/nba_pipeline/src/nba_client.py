import requests
import os
import time

class NBAClient:
    def __init__(self, api_key: str = None, host: str = None):
        self.api_key = api_key or os.getenv("NBA_API_KEY")
        self.host = host or os.getenv("NBA_API_HOST", "api-nba-v1.p.rapidapi.com")
        self.base_url = f"https://{self.host}"

        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        for attempt in range(5):  # max 5 essais
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 429:
                wait_time = (attempt + 1) * 5
                print(f"🚦 Rate limit hit (attempt {attempt + 1}). Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            response.raise_for_status()
            return response.json().get("response", [])
        raise Exception("Too many requests - retry attempts failed.")

    def get_games(self, season, game_type="Regular Season"):
        return self._make_request("games", {
            "season": season,
            "type": game_type
        })

    def get_players(self, season):
        return self._make_request("players", {"season": season})

    def get_seasons(self):
        return self._make_request("seasons")

    def get_teams(self):
        return self._make_request("teams")

    def get_draft(self, season):
        return self._make_request("players", {"season": season})
