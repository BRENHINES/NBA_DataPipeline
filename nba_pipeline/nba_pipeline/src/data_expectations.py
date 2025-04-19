import great_expectations as ge
import polars as pl

def validate_seasons(seasons: list[str]) -> bool:
    # Convertir la liste en dataframe Polars
    df = pl.DataFrame({"season": seasons})

    # Convertir en Pandas pour compatibilité temporaire avec GE
    gdf = ge.from_pandas(df.to_pandas())

    # Définir les attentes
    gdf.expect_column_values_to_match_regex("season", r"^20\\d{2}$")
    gdf.expect_column_values_to_be_unique("season")
    gdf.expect_column_values_to_not_be_null("season")

    # Exécuter la validation
    results = gdf.validate()
    return results["success"]
