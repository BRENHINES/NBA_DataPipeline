from dagster import asset
import polars as pl
import joblib
from pathlib import Path
from nba_pipeline.nba_pipeline.models.features.draft_features import build_draft_dataset

@asset(required_resource_keys={"db"}, deps=[
    "draft_by_season",
    "player_stats_by_season",
    "enrich_player_stats_with_kpis"
])
def predict_draft_flops(context):
    # Charger le modèle entraîné
    model_path = Path(__file__).resolve().parents[1] / "models/saved_model/draft_flop_model.pkl"
    model = joblib.load(model_path)

    # Charger le dataset
    df = build_draft_dataset().to_pandas()
    df = df.dropna()

    # Features utilisées
    features = [
        "round", "pick", "avg_points",
        "avg_assists", "avg_rebounds",
        "avg_efficiency", "avg_minutes"
    ]
    X = df[features]

    # Prédictions
    probas = model.predict_proba(X)[:, 1]  # Proba d'être un flop
    predictions = model.predict(X)

    # Ajouter les colonnes
    df["prob_flop"] = probas
    df["is_flop_predicted"] = predictions

    # Connexion DB
    conn = context.resources.db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nba_draft_predictions (
            player_id INT,
            season TEXT,
            prob_flop FLOAT,
            is_flop_predicted INT,
            PRIMARY KEY (player_id, season)
        );
    """)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO nba_draft_predictions (player_id, season, prob_flop, is_flop_predicted)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (player_id, season) DO UPDATE SET
              prob_flop = EXCLUDED.prob_flop,
              is_flop_predicted = EXCLUDED.is_flop_predicted;
        """, (
            row["player_id"], row["season"],
            float(row["prob_flop"]),
            int(row["is_flop_predicted"])
        ))

    conn.commit()
    cursor.close()
    conn.close()
    context.log.info("✅ Prédictions de flops insérées en base.")

    return df
