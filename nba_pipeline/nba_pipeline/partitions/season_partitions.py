from dagster import DynamicPartitionsDefinition

# Partition dynamique nommée "nba_seasons"
season_partitions_def = DynamicPartitionsDefinition(name="nba_seasons")
