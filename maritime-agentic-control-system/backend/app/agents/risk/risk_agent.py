from typing import Any, Dict, Optional

<<<<<<< HEAD
from app.agents.risk.risk_model import RiskModel


class RiskAgent:
    """
    Maritime risk assessment agent.

    Combines incoming event and route context into a feature vector
    and uses the trained Random Forest model to predict a risk score.
    """

    SEVERITY_TO_WEATHER = {
        "critical": 1.0,
        "high": 0.8,
        "warning": 0.6,
        "medium": 0.45,
        "low": 0.2,
        "info": 0.05,
    }

    def __init__(self):
        self.risk_model = RiskModel()

=======

class RiskAgent:
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
    def calculate_risk(
        self,
        event: Dict[str, Any],
        route: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
<<<<<<< HEAD

        severity = self._normalize_severity(event.get("severity"))

        features = self._build_features(
            event=event,
            route=route,
            severity=severity,
        )

        score = self.risk_model.predict(features)

=======
        severity = self._normalize_severity(event.get("severity"))
        score = self._calculate_score(severity, route)
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
        return {
            "score": score,
            "severity": severity,
            "likelihood": self._likelihood_from_score(score),
            "impact": self._impact_from_severity(severity),
            "category": event.get("event_type", "operational"),
            "description": event.get("description"),
<<<<<<< HEAD
            "features_used": features,
        }

    def _build_features(
        self,
        event: Dict[str, Any],
        route: Optional[Dict[str, Any]],
        severity: str,
    ) -> Dict[str, float]:

        defaults = self.risk_model.feature_defaults

        features = {
            "distance_nm": self._get_numeric_value(
                route,
                ["distance_nm", "distance"],
                defaults["distance_nm"],
            ),

            "estimated_cost_usd": self._get_numeric_value(
                route,
                ["estimated_cost_usd", "estimated_cost", "cost"],
                defaults["estimated_cost_usd"],
            ),

            "delay_hours": self._get_numeric_value(
                event,
                ["delay_hours", "estimated_delay_hours"],
                self._get_numeric_value(
                    route,
                    ["delay_hours", "estimated_delay_hours"],
                    defaults["delay_hours"],
                ),
            ),

            "weather_severity": self._get_numeric_value(
                event,
                ["weather_severity"],
                self.SEVERITY_TO_WEATHER[severity],
            ),

            "congestion_score": self._get_numeric_value(
                event,
                ["congestion_score"],
                defaults["congestion_score"],
            ),

            "incident_score": self._get_numeric_value(
                event,
                ["incident_score"],
                defaults["incident_score"],
            ),
        }

        return {
            feature: self._validate_feature(
                feature,
                value,
            )
            for feature, value in features.items()
        }

    def _get_numeric_value(
        self,
        source: Optional[Dict[str, Any]],
        keys,
        default: float,
    ) -> float:

        if not source:
            return float(default)

        for key in keys:
            value = source.get(key)

            if value is not None:
                try:
                    return float(value)
                except (TypeError, ValueError):
                    continue

        return float(default)

    def _validate_feature(
        self,
        feature: str,
        value: float,
    ) -> float:

        value = float(value)

        normalized_features = {
            "weather_severity",
            "congestion_score",
            "incident_score",
        }

        if feature in normalized_features:
            return max(0.0, min(1.0, value))

        return max(0.0, value)

    def _normalize_severity(self, severity: Any) -> str:

        if not severity:
            return "info"

        text = str(severity).strip().lower()

        valid_values = {
            "critical",
            "high",
            "warning",
            "warn",
            "medium",
            "low",
            "info",
        }

        if text in valid_values:
            return "warning" if text == "warn" else text

        return "info"

    def _likelihood_from_score(self, score: float) -> str:

        if score >= 75:
            return "high"

        if score >= 40:
            return "medium"

        return "low"

    def _impact_from_severity(
        self,
        severity: str,
    ) -> str:

        if severity in {"critical", "high"}:
            return "high"

        if severity == "warning":
            return "medium"

=======
        }

    def _normalize_severity(self, severity: Any) -> str:
        if not severity:
            return "info"
        text = str(severity).strip().lower()
        if text in {"critical", "high", "warning", "warn", "medium", "low", "info"}:
            return "warning" if text == "warn" else text
        return "info"

    def _severity_score(self, severity: str) -> int:
        mapping = {
            "critical": 90,
            "high": 75,
            "warning": 50,
            "medium": 30,
            "low": 15,
            "info": 5,
        }
        return mapping.get(severity, 5)

    def _route_risk_modifier(self, route: Optional[Dict[str, Any]]) -> int:
        if not route:
            return 0
        modifier = 0
        status = str(route.get("status", "")).strip().lower()
        if status in {"planned", "pending"}:
            modifier += 5
        elif status in {"in_progress", "active"}:
            modifier += 15
        elif status in {"failed", "delayed"}:
            modifier += 25

        waypoints = route.get("waypoints")
        if isinstance(waypoints, str) and waypoints:
            modifier += min(10, waypoints.count(",") + 1)
        elif isinstance(waypoints, list):
            modifier += min(10, len(waypoints))

        return modifier

    def _calculate_score(
        self,
        severity: str,
        route: Optional[Dict[str, Any]],
    ) -> int:
        score = self._severity_score(severity) + self._route_risk_modifier(route)
        return max(0, min(100, score))

    def _likelihood_from_score(self, score: int) -> str:
        if score >= 75:
            return "high"
        if score >= 40:
            return "medium"
        return "low"

    def _impact_from_severity(self, severity: str) -> str:
        if severity in {"critical", "high"}:
            return "high"
        if severity == "warning":
            return "medium"
        return "low"
from typing import Any, Dict, Optional


class RiskAgent:
    def calculate_risk(
        self,
        event: Dict[str, Any],
        route: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        severity = self._normalize_severity(event.get("severity"))
        score = self._calculate_score(severity, route)
        return {
            "score": score,
            "severity": severity,
            "likelihood": self._likelihood_from_score(score),
            "impact": self._impact_from_severity(severity),
            "category": event.get("event_type", "operational"),
            "description": event.get("description"),
        }

    def _normalize_severity(self, severity: Any) -> str:
        if not severity:
            return "info"
        text = str(severity).strip().lower()
        if text in {"critical", "high", "warning", "warn", "medium", "low", "info"}:
            return "warning" if text == "warn" else text
        return "info"

    def _severity_score(self, severity: str) -> int:
        mapping = {
            "critical": 90,
            "high": 75,
            "warning": 50,
            "medium": 30,
            "low": 15,
            "info": 5,
        }
        return mapping.get(severity, 5)

    def _route_risk_modifier(self, route: Optional[Dict[str, Any]]) -> int:
        if not route:
            return 0
        modifier = 0
        status = str(route.get("status", "")).strip().lower()
        if status in {"planned", "pending"}:
            modifier += 5
        elif status in {"in_progress", "active"}:
            modifier += 15
        elif status in {"failed", "delayed"}:
            modifier += 25

        waypoints = route.get("waypoints")
        if isinstance(waypoints, str) and waypoints:
            modifier += min(10, waypoints.count(",") + 1)
        elif isinstance(waypoints, list):
            modifier += min(10, len(waypoints))

        return modifier

    def _calculate_score(
        self,
        severity: str,
        route: Optional[Dict[str, Any]],
    ) -> int:
        score = self._severity_score(severity) + self._route_risk_modifier(route)
        return max(0, min(100, score))

    def _likelihood_from_score(self, score: int) -> str:
        if score >= 75:
            return "high"
        if score >= 40:
            return "medium"
        return "low"

    def _impact_from_severity(self, severity: str) -> str:
        if severity in {"critical", "high"}:
            return "high"
        if severity == "warning":
            return "medium"
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
        return "low"