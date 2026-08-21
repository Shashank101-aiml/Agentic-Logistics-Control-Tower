from pathlib import Path
import sys
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# -------------------------------------------------
# Project paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DATA_PATH = PROJECT_DIR / "data" / "raw" / "maritime_routes.csv"
TRAINING_DATA_PATH = PROJECT_DIR / "data" / "risk_training_data.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "risk_model.joblib"


# -------------------------------------------------
# Generate reproducible training data
# -------------------------------------------------

def generate_training_data(df, samples_per_route=100, random_state=42):
    rng = np.random.default_rng(random_state)

    records = []

    for _, route in df.iterrows():

        for _ in range(samples_per_route):

            weather_severity = np.clip(
                route["weather_severity"] + rng.normal(0, 0.10),
                0,
                1
            )

            congestion_score = np.clip(
                route["congestion_score"] + rng.normal(0, 0.12),
                0,
                1
            )

            incident_score = np.clip(
                route["incident_score"] + rng.normal(0, 0.08),
                0,
                1
            )

            delay_hours = max(
                0,
                route["base_delay_hours"] * rng.uniform(0.75, 1.50)
            )

            distance_nm = route["distance_nm"]

            estimated_cost_usd = max(
                0,
                route["estimated_cost_usd"] * rng.uniform(0.90, 1.25)
            )

            # Synthetic target generation for reproducible model training
            risk_score = (
                weather_severity * 35
                + congestion_score * 20
                + incident_score * 30
                + min(delay_hours / 200, 1) * 10
                + min(distance_nm / 7000, 1) * 5
                + rng.normal(0, 3)
            )

            risk_score = np.clip(risk_score, 0, 100)

            records.append({
                "distance_nm": distance_nm,
                "estimated_cost_usd": estimated_cost_usd,
                "delay_hours": delay_hours,
                "weather_severity": weather_severity,
                "congestion_score": congestion_score,
                "incident_score": incident_score,
                "risk_score": risk_score
            })

    return pd.DataFrame(records)


# -------------------------------------------------
# Train Random Forest
# -------------------------------------------------

def train_model():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Route dataset not found: {DATA_PATH}"
        )

    routes_df = pd.read_csv(DATA_PATH)

    training_df = generate_training_data(routes_df)

    TRAINING_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    training_df.to_csv(
        TRAINING_DATA_PATH,
        index=False
    )

    feature_columns = [
        "distance_nm",
        "estimated_cost_usd",
        "delay_hours",
        "weather_severity",
        "congestion_score",
        "incident_score"
    ]

    X = training_df[feature_columns]
    y = training_df["risk_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model_bundle = {
    "model": model,
    "features": feature_columns,
    "feature_defaults": {
        column: float(X[column].median())
        for column in feature_columns
    }
}

    joblib.dump(
        model_bundle,
        MODEL_PATH
    )

    print("\nTraining completed successfully\n")

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    print("\nModel Evaluation:")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²:   {r2:.4f}")

    print(f"\nModel saved to:\n{MODEL_PATH}")

    print("\nFeature Importance:")

    importance = pd.Series(
        model.feature_importances_,
        index=feature_columns
    ).sort_values(ascending=False)

    print(importance)


if __name__ == "__main__":
    train_model()