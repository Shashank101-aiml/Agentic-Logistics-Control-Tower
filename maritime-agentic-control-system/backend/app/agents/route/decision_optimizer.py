from typing import Any, Dict, List, Optional

from app.agents.route.decision_config import DecisionWeights


class RouteDecisionOptimizer:
    """
    Ranks multiple candidate routes using weighted multi-criteria
    decision analysis.

    Lower values for risk, cost, delay, and distance are considered
    preferable.
    """

    REQUIRED_METRICS = {
        "risk_score",
        "estimated_cost_usd",
        "estimated_delay_hours",
        "total_distance_nm",
    }

    def __init__(
        self,
        weights: Optional[DecisionWeights] = None,
    ):
        self.weights = weights or DecisionWeights()
        self.weights.validate()

    def rank_routes(
        self,
        routes: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        if not routes:
            return []

        self._validate_routes(routes)

        normalized_routes = self._normalize_metrics(routes)

        ranked_routes = []

        for route, normalized in zip(
            routes,
            normalized_routes,
        ):
            decision_score = self._calculate_score(
                normalized
            )

            ranked_routes.append(
                {
                    **route,
                    "decision_score": round(
                        decision_score,
                        4,
                    ),
                    "decision_breakdown": {
                        "risk": round(
                            normalized["risk_score"]
                            * self.weights.risk,
                            4,
                        ),
                        "cost": round(
                            normalized["estimated_cost_usd"]
                            * self.weights.cost,
                            4,
                        ),
                        "delay": round(
                            normalized[
                                "estimated_delay_hours"
                            ]
                            * self.weights.delay,
                            4,
                        ),
                        "distance": round(
                            normalized[
                                "total_distance_nm"
                            ]
                            * self.weights.distance,
                            4,
                        ),
                    },
                }
            )

        ranked_routes.sort(
            key=lambda route: route["decision_score"],
            reverse=True,
        )

        for rank, route in enumerate(
            ranked_routes,
            start=1,
        ):
            route["rank"] = rank

        return ranked_routes

    def select_best_route(
        self,
        routes: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:

        ranked_routes = self.rank_routes(routes)

        if not ranked_routes:
            return None

        return ranked_routes[0]

    def _validate_routes(
        self,
        routes: List[Dict[str, Any]],
    ) -> None:

        for index, route in enumerate(routes):

            missing = (
                self.REQUIRED_METRICS
                - set(route.keys())
            )

            if missing:
                raise ValueError(
                    f"Route at index {index} is missing "
                    f"required metrics: {sorted(missing)}"
                )

    def _normalize_metrics(
        self,
        routes: List[Dict[str, Any]],
    ) -> List[Dict[str, float]]:

        metric_values = {
            metric: [
                float(route[metric])
                for route in routes
            ]
            for metric in self.REQUIRED_METRICS
        }

        normalized_routes = []

        for route in routes:

            normalized = {}

            for metric, values in metric_values.items():

                value = float(route[metric])

                minimum = min(values)
                maximum = max(values)

                if maximum == minimum:
                    normalized[metric] = 1.0
                else:
                    # Lower operational values are better.
                    normalized[metric] = (
                        (maximum - value)
                        / (maximum - minimum)
                    )

            normalized_routes.append(normalized)

        return normalized_routes

    def _calculate_score(
        self,
        normalized: Dict[str, float],
    ) -> float:

        return (
            normalized["risk_score"]
            * self.weights.risk
            + normalized["estimated_cost_usd"]
            * self.weights.cost
            + normalized["estimated_delay_hours"]
            * self.weights.delay
            + normalized["total_distance_nm"]
            * self.weights.distance
        )