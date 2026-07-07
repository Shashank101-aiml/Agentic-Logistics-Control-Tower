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
        return "low"