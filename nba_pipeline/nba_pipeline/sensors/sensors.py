from dagster import SensorDefinition, RunRequest
from datetime import datetime
from nba_pipeline.nba_pipeline.resources.api_ressources import NBAAPIResource

import pytz

# Vérifie chaque jour s'il y a des matchs à venir dans la journée

def match_day_sensor_fn(context):
    client = NBAAPIResource()
    today = datetime.now(pytz.UTC).date().isoformat()
    games = client.get_games_by_date(today)

    if games:
        context.log.info(f"{len(games)} matchs détectés pour {today}.")
        return [
            RunRequest(
                run_key=f"games-stats-{today}",
                run_config={
                    "ops": {
                        "games_by_season": {},
                        "player_stats_by_season": {}
                    }
                },
                tags={"triggered_by": "sensor", "date": today}
            )
        ]
    else:
        context.log.info(f"Aucun match prévu le {today}.")
        return []

match_day_sensor = SensorDefinition(
    name="match_day_sensor",
    evaluation_fn=match_day_sensor_fn,
    minimum_interval_seconds=3600 * 3  # Vérifie tous les jours à 3h UTC
)
