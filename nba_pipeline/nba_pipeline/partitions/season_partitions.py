from dagster import DynamicPartitionsDefinition, StaticPartitionsDefinition

# Partition dynamique nommée "nba_seasons"
season_partition_def = DynamicPartitionsDefinition(name="nba_teams_partition")