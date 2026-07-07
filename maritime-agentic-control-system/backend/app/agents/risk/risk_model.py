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