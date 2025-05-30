import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path
import joblib

from nba_pipeline.nba_pipeline.models.features.playoffs_profiles import build_playoffs_dataset

def train_playoffs_predictor(context):
    # Charger les données
    df = build_playoffs_dataset().to_pandas()

    # Séparation X/y
    X = df.drop(columns=["home_win"])
    y = df["home_win"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Évaluation
    y_pred = model.predict(X_test)
    context.log.info("\n📊 Rapport de classification :\n")
    context.log.info(classification_report(y_test, y_pred))
    context.log.info("\n📊 Matrice de confusion :\n")
    context.log.info(confusion_matrix(y_test, y_pred))

    # Sauvegarde du modèle
    model_path = Path(__file__).resolve().parent / "saved_model/playoffs_predictor.pkl"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    context.log.info(f"✅ Modèle sauvegardé : {model_path}")

    return model

def save_model(context, model, model_name="draft_flop_model.pkl"):
    save_path = Path(__file__).resolve().parent / "saved_model"
    save_path.mkdir(parents=True, exist_ok=True)
    model_path = save_path / model_name
    joblib.dump(model, model_path)
    context.log.info(f"Modèle sauvegardé ici : {model_path}")
    return model_path

if __name__ == "__main__":
    train_playoffs_predictor()