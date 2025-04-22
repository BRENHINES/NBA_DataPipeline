# tests/test_nba_client.py

from nba_pipeline.nba_pipeline.src.nba_client import NBAClient
from dotenv import load_dotenv

load_dotenv()

def test_get_seasons():
    client = NBAClient()
    seasons = client.get_seasons()
    assert isinstance(seasons, list)
    assert '2015' in seasons or '2016' in seasons
