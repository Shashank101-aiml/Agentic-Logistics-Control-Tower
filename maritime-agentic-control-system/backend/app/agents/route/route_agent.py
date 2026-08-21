from typing import Any, Dict, Optional

<<<<<<< HEAD
from app.agents.route.alternatives import RouteAlternatives
from app.agents.route.decision_optimizer import RouteDecisionOptimizer
from app.agents.route.optimizer import RouteOptimizer


class RouteAgent:
    """
    Route intelligence agent.

    Supports:
    - Dijkstra / A* route optimization
    - Multiple real route alternatives
    - Weighted multi-criteria decision optimization
    - Backward-compatible fallback recommendations
    """

    def __init__(self) -> None:
        self.optimizer = RouteOptimizer()
        self.alternatives = RouteAlternatives()
        self.decision_optimizer = RouteDecisionOptimizer()

=======

class RouteAgent:
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
    def suggest_route(
        self,
        risk_score: Any,
        current_route: Optional[Dict[str, Any]] = None,
<<<<<<< HEAD
    ) -> Dict[str, Any]:
        """
        Suggest the best route.

        If origin and destination are available, the agent uses the
        NetworkX graph, generates real route alternatives, and ranks
        them using weighted decision optimization.

        If route information is unavailable, a backward-compatible
        recommendation is returned.
        """

        risk_value = self._extract_risk_score(risk_score)

        current_route = current_route or {}

        origin = current_route.get("origin")
        destination = current_route.get("destination")

        # Use the real routing system when route context is available.
        if origin and destination:
            return self._intelligent_route_selection(
                current_route=current_route,
                risk_value=risk_value,
            )

        # Backward-compatible fallback for existing project workflows.
        return self._fallback_recommendation(risk_value)

    def suggest_route_from_context(
        self,
        risk_score: Any,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        route_status: Optional[str] = None,
    ) -> Dict[str, Any]:

        route = {
            "origin": origin,
            "destination": destination,
            "status": route_status or "planned",
        }

        return self.suggest_route(
            risk_score=risk_score,
            current_route=route,
        )

    def _intelligent_route_selection(
        self,
        current_route: Dict[str, Any],
        risk_value: float,
    ) -> Dict[str, Any]:

        alternatives = self.alternatives.generate_alternatives(
            route=current_route,
            count=3,
            weight_metric="risk",
        )

        if not alternatives:
            return self._fallback_recommendation(risk_value)

        ranked_routes = self.decision_optimizer.rank_routes(
            alternatives
        )

        best_route = ranked_routes[0]

        return {
            "route": best_route.get("name"),
            "reason": self._build_reason(
                best_route,
                risk_value,
            ),
            "best_route": best_route,
            "alternatives": ranked_routes,
            "decision": {
                "selected_rank": best_route.get("rank"),
                "decision_score": best_route.get(
                    "decision_score"
                ),
                "selection_method": (
                    "networkx route alternatives "
                    "+ weighted decision optimization"
                ),
            },
        }

    def _extract_risk_score(
        self,
        risk_score: Any,
    ) -> float:
        """
        Handles both numeric risk scores and dictionaries returned
        by RiskAgent.
        """

        if isinstance(risk_score, dict):
            return float(
                risk_score.get(
                    "score",
                    risk_score.get("risk_score", 0),
                )
            )

        try:
            return float(risk_score)
        except (TypeError, ValueError):
            return 0.0

    def _build_reason(
        self,
        route: Dict[str, Any],
        risk_value: float,
    ) -> str:

        return (
            f"Selected as the best overall route after evaluating "
            f"risk, cost, delay, and distance. "
            f"Current event risk score: {round(risk_value, 2)}. "
            f"Route risk score: {route.get('risk_score')}. "
            f"Decision score: {route.get('decision_score')}."
        )

    def _fallback_recommendation(
        self,
        risk_score: float,
    ) -> Dict[str, Any]:
        """
        Preserves the previous behavior when no origin/destination
        information is available.
        """

        if risk_score >= 90:
            return {
                "route": "Cape of Good Hope",
                "reason": (
                    "Extreme risk detected. Recommend a longer "
                    "but safer passage to avoid severe conditions."
                ),
=======
    ) -> Dict[str, str]:
        if isinstance(risk_score, dict):
            risk_score = risk_score.get("score", 50)
        try:
            risk_score = float(risk_score)
        except (TypeError, ValueError):
            risk_score = 50.0

        if risk_score >= 90:
            return {
                "route": "Cape of Good Hope Bypass",
                "reason": "Extreme risk detected. Recommend a longer but safer passage to avoid severe condition cell."
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
            }

        if risk_score >= 70:
            return {
<<<<<<< HEAD
                "route": "Horn of Africa",
                "reason": (
                    "High risk conditions present. Use a more "
                    "conservative route with established safety margins."
                ),
=======
                "route": "Corridor Beta (Southern Bypass)",
                "reason": "High risk conditions present. Shifting waypoints 120 nm south to bypass severe weather system."
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
            }

        if risk_score >= 40:
            return {
<<<<<<< HEAD
                "route": "Suez Canal",
                "reason": (
                    "Moderate risk. Proceed with caution on the "
                    "standard commercial channel."
                ),
            }

        return {
            "route": "Panama Canal",
            "reason": (
                "Low risk conditions. Use the fastest and most "
                "direct route."
            ),
        }
=======
                "route": "Suez Canal Commercial Passage",
                "reason": "Moderate risk. Proceed with caution along standard commercial channel."
            }

        return {
            "route": "Direct Deepwater Corridor",
            "reason": "Low risk conditions. Optimal direct high-speed navigation route."
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
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
