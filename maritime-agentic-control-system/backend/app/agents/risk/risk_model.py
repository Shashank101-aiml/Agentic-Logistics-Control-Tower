from pathlib import Path

import joblib
import pandas as pd


class RiskModel:
    """
    Loads the trained Random Forest model and performs
    risk prediction from route/event features.
    """

    def __init__(self):
        backend_dir = Path(__file__).resolve().parents[3]
        model_path = backend_dir / "models" / "risk_model.joblib"

        if not model_path.exists():
            raise FileNotFoundError(
                f"Trained risk model not found at: {model_path}. "
                "Run train_risk_model.py first."
            )

        model_bundle = joblib.load(model_path)

        self.model = model_bundle["model"]
        self.feature_columns = model_bundle["features"]
        self.feature_defaults = model_bundle.get(
            "feature_defaults",
            {}
        )

    def predict(self, features: dict) -> float:
        """
        Predict a maritime route risk score.

        Parameters
        ----------
        features : dict
            Dictionary containing all required model features.

        Returns
        -------
        float
            Predicted risk score between 0 and 100.
        """

        missing_features = [
            feature
            for feature in self.feature_columns
            if feature not in features
        ]

        if missing_features:
            raise ValueError(
                f"Missing required risk features: {missing_features}"
            )

        input_df = pd.DataFrame(
            [{feature: features[feature] for feature in self.feature_columns}]
        )

        prediction = float(self.model.predict(input_df)[0])

        return round(max(0.0, min(100.0, prediction)), 2)

    def get_feature_importance(self) -> dict:
        """
        Returns feature importance from the trained Random Forest.
        """

        importance = self.model.feature_importances_

        return {
            feature: round(float(score), 4)
            for feature, score in zip(
                self.feature_columns,
                importance
            )
        }