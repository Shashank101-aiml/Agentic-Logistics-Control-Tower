from typing import Any, Dict, Optional


class RouteAgent:
    def suggest_route(
        self,
        risk_score: float,
        current_route: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        if risk_score >= 90:
            return {
                "route": "Cape of Good Hope",
                "reason": "Extreme risk detected. Recommend a longer but safer passage to avoid severe conditions."
            }

        if risk_score >= 70:
            return {
                "route": "Horn of Africa",
                "reason": "High risk conditions present. Use a more conservative route with established safety margins."
            }

        if risk_score >= 40:
            return {
                "route": "Suez Canal",
                "reason": "Moderate risk. Proceed with caution on the standard commercial channel."
            }

        return {
            "route": "Panama Canal",
            "reason": "Low risk conditions. Use the fastest and most direct route."
        }

    def suggest_route_from_context(
        self,
        risk_score: float,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        route_status: Optional[str] = None,
    ) -> Dict[str, str]:
        recommendation = self.suggest_route(risk_score)

        if route_status and route_status.lower() in {"in_progress", "active"}:
            recommendation["reason"] += " Current route is already active, so update cautiously."

        if origin and destination:
            recommendation["reason"] += f" Origin: {origin}, destination: {destination}."

        return recommendation