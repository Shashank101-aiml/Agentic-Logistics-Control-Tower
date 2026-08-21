<<<<<<< HEAD
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
=======
from typing import Any, Dict, Optional

from app.agents.risk.feature_engineering import FeatureEngineer


class RiskModel:
    def __init__(self, weights: Optional[Dict[str, float]] = None) -> None:
        default_weights: Dict[str, float] = {
            "event_severity_score": 0.30,
            "route_status_score": 0.20,
            "risk_likelihood_score": 0.20,
            "risk_impact_score": 0.20,
            "route_waypoint_count": 0.05,
            "event_has_description": 0.02,
            "event_source_provided": 0.02,
            "route_has_origin": 0.01,
            "route_has_destination": 0.01,
            "route_notes_provided": 0.01,
            "risk_has_mitigation_plan": 0.03,
            "risk_is_active": 0.05,
        }
        self.weights = {**default_weights, **(weights or {})}

    def predict(
        self,
        event: Dict[str, Any],
        route: Optional[Dict[str, Any]] = None,
        risk: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        features = FeatureEngineer.combine_features(
            event=event, route=route, risk=risk
        )
        score = self._calculate_score(features)
        return {
            "score": score,
            "risk_level": self._risk_level(score),
            "likelihood": self._likelihood(score),
            "impact": self._impact(score),
            "features": features,
        }

    def _calculate_score(self, features: Dict[str, Any]) -> int:
        total = 0.0
        for name, value in features.items():
            weight = self.weights.get(name)
            if weight is None:
                continue
            if isinstance(value, bool):
                value = 1 if value else 0
            if isinstance(value, (int, float)):
                total += float(value) * weight

        score = int(round(max(0.0, min(100.0, total * 10.0))))
        return score

    def _risk_level(self, score: int) -> str:
        if score >= 75:
            return "high"
        if score >= 40:
            return "medium"
        return "low"

    def _likelihood(self, score: int) -> str:
        if score >= 70:
            return "high"
        if score >= 45:
            return "medium"
        return "low"

    def _impact(self, score: int) -> str:
        if score >= 80:
            return "critical"
        if score >= 55:
            return "high"
        if score >= 30:
            return "medium"
        return "low"
from typing import Any, Dict, Optional

from app.agents.risk.feature_engineering import FeatureEngineer


class RiskModel:
    def __init__(self, weights: Optional[Dict[str, float]] = None) -> None:
        default_weights: Dict[str, float] = {
            "event_severity_score": 0.30,
            "route_status_score": 0.20,
            "risk_likelihood_score": 0.20,
            "risk_impact_score": 0.20,
            "route_waypoint_count": 0.05,
            "event_has_description": 0.02,
            "event_source_provided": 0.02,
            "route_has_origin": 0.01,
            "route_has_destination": 0.01,
            "route_notes_provided": 0.01,
            "risk_has_mitigation_plan": 0.03,
            "risk_is_active": 0.05,
        }
        self.weights = {**default_weights, **(weights or {})}

    def predict(
        self,
        event: Dict[str, Any],
        route: Optional[Dict[str, Any]] = None,
        risk: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        features = FeatureEngineer.combine_features(
            event=event, route=route, risk=risk
        )
        score = self._calculate_score(features)
        return {
            "score": score,
            "risk_level": self._risk_level(score),
            "likelihood": self._likelihood(score),
            "impact": self._impact(score),
            "features": features,
        }

    def _calculate_score(self, features: Dict[str, Any]) -> int:
        total = 0.0
        for name, value in features.items():
            weight = self.weights.get(name)
            if weight is None:
                continue
            if isinstance(value, bool):
                value = 1 if value else 0
            if isinstance(value, (int, float)):
                total += float(value) * weight

        score = int(round(max(0.0, min(100.0, total * 10.0))))
        return score

    def _risk_level(self, score: int) -> str:
        if score >= 75:
            return "high"
        if score >= 40:
            return "medium"
        return "low"

    def _likelihood(self, score: int) -> str:
        if score >= 70:
            return "high"
        if score >= 45:
            return "medium"
        return "low"

    def _impact(self, score: int) -> str:
        if score >= 80:
            return "critical"
        if score >= 55:
            return "high"
        if score >= 30:
            return "medium"
        return "low"
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
