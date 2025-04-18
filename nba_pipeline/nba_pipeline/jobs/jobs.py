from dagster import define_asset_job

# Le job exécute uniquement les assets déclarés
extract_job = define_asset_job(name="extract_seasons_job", selection=["available_seasons"])
