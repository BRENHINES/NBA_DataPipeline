import joblib
from pathlib import Path
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from nba_pipeline.nba_pipeline.models.features.draft_features import build_draft_dataset


def train_draft_model(context):
    # Charger le dataset
    df = build_draft_dataset()

    # Convertir en DataFrame Pandas pour sklearn / XGBoost
    df_pd = df.to_pandas()
    df_pd = df_pd.dropna()  # Suppression des lignes incomplètes

    # Features et label
    features = [
        "round", "pick", "avg_points",
        "avg_assists", "avg_rebounds",
        "avg_efficiency", "avg_minutes"
    ]
    X = df_pd[features]
    y = df_pd["is_flop"]

    # Split des données
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Entraînement
    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X_train, y_train)
    save_model(model)

    # Prédictions
    y_pred = model.predict(X_test)

    # Évaluation
    context.log.info("Classification Report :\n")
    context.log.info(classification_report(y_test, y_pred))

    context.log.info("Matrice de confusion :\n")
    context.log.info(confusion_matrix(y_test, y_pred))

    return model

def save_model(context, model, model_name="draft_flop_model.pkl"):
    save_path = Path(__file__).resolve().parent / "saved_model"
    save_path.mkdir(parents=True, exist_ok=True)
    model_path = save_path / model_name
    joblib.dump(model, model_path)
    context.log.info(f"Modèle sauvegardé ici : {model_path}")
    return model_path

