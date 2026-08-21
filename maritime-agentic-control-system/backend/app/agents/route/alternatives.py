from typing import Any, Dict, List, Optional

<<<<<<< HEAD
import networkx as nx

from app.agents.route.logistics_graph import LogisticsGraph


class RouteAlternatives:
    """
    Generates genuine alternative maritime routes using the logistics graph.

    Alternatives are discovered from valid graph paths instead of rotating
    waypoints or using hardcoded route variations.
    """

    def __init__(self) -> None:
        self.logistics_graph = LogisticsGraph()
        self.graph = self.logistics_graph.get_graph()

=======

class RouteAlternatives:
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
    def generate_alternatives(
        self,
        route: Dict[str, Any],
        count: int = 3,
<<<<<<< HEAD
        weight_metric: str = "risk",
    ) -> List[Dict[str, Any]]:

        origin = route.get("origin")
        destination = route.get("destination")

        if not origin or not destination:
            raise ValueError(
                "Route must contain both 'origin' and 'destination'."
            )

        if origin not in self.graph:
            raise ValueError(f"Origin port not found: {origin}")

        if destination not in self.graph:
            raise ValueError(f"Destination port not found: {destination}")

        weight_function = self._get_weight_function(weight_metric)

        try:
            paths = nx.shortest_simple_paths(
                self.graph,
                source=origin,
                target=destination,
                weight=weight_function,
            )
        except nx.NetworkXNoPath:
            return []

        alternatives = []

        for index, path in enumerate(paths, start=1):

            if len(alternatives) >= count:
                break

            alternative = self._build_alternative(
                path=path,
                index=index,
                status=route.get("status", "planned"),
                weight_metric=weight_metric,
            )

=======
    ) -> List[Dict[str, Any]]:
        base_origin = route.get("origin", "unknown origin")
        base_destination = route.get("destination", "unknown destination")
        waypoints = route.get("waypoints") or []
        status = route.get("status", "planned")

        alternatives = []
        for idx in range(1, count + 1):
            alternative = self._build_alternative(
                origin=base_origin,
                destination=base_destination,
                waypoints=waypoints,
                status=status,
                index=idx,
            )
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
            alternatives.append(alternative)

        return alternatives

<<<<<<< HEAD
    def _get_weight_function(self, metric: str):

        metric = metric.lower()

        def weight(
            source: str,
            target: str,
            data: Dict[str, Any],
        ) -> float:

            distance = float(data.get("distance_nm", 0))
            cost = float(data.get("estimated_cost_usd", 0))
            delay = float(
                data.get(
                    "delay_hours",
                    data.get("base_delay_hours", 0),
                )
            )

            weather = float(data.get("weather_severity", 0))
            congestion = float(data.get("congestion_score", 0))
            incident = float(data.get("incident_score", 0))

            risk = (
                weather * 0.45
                + congestion * 0.30
                + incident * 0.25
            )

            if metric == "distance":
                return distance

            if metric == "cost":
                return cost

            if metric == "delay":
                return delay

            if metric == "risk":
                return distance * (1 + risk)

            return distance

        return weight

    def _build_alternative(
        self,
        path: List[str],
        index: int,
        status: str,
        weight_metric: str,
    ) -> Dict[str, Any]:

        metrics = self._calculate_path_metrics(path)

        waypoints = []

        for port_id in path:
            port = self.logistics_graph.get_port(port_id)

            if port:
                waypoints.append(
                    {
                        "port_id": port_id,
                        "label": port.get(
                            "port_name",
                            port_id,
                        ),
                        "country": port.get("country"),
                        "latitude": port.get("latitude"),
                        "longitude": port.get("longitude"),
                    }
                )

        return {
            "name": f"Alternative Route {index}",
            "alternative_index": index,
            "origin": path[0],
            "destination": path[-1],
            "status": status,
            "waypoints": waypoints,
            "path": path,
            "optimized": True,
            "algorithm": "k-shortest-paths",
            "weight_metric": weight_metric,
            **metrics,
        }

    def _calculate_path_metrics(
        self,
        path: List[str],
    ) -> Dict[str, float]:

        total_distance = 0.0
        total_cost = 0.0
        total_delay = 0.0

        weather_values = []
        congestion_values = []
        incident_values = []

        for source, target in zip(path[:-1], path[1:]):

            data = self.graph.get_edge_data(source, target)

            if not data:
                continue

            total_distance += float(
                data.get("distance_nm", 0)
            )

            total_cost += float(
                data.get("estimated_cost_usd", 0)
            )

            total_delay += float(
                data.get(
                    "delay_hours",
                    data.get("base_delay_hours", 0),
                )
            )

            weather_values.append(
                float(data.get("weather_severity", 0))
            )

            congestion_values.append(
                float(data.get("congestion_score", 0))
            )

            incident_values.append(
                float(data.get("incident_score", 0))
            )

        risk_score = (
            self._average(weather_values) * 45
            + self._average(congestion_values) * 30
            + self._average(incident_values) * 25
        )

        return {
            "total_distance_nm": round(total_distance, 2),
            "estimated_cost_usd": round(total_cost, 2),
            "estimated_delay_hours": round(total_delay, 2),
            "average_weather_severity": round(
                self._average(weather_values), 4
            ),
            "average_congestion_score": round(
                self._average(congestion_values), 4
            ),
            "average_incident_score": round(
                self._average(incident_values), 4
            ),
            "risk_score": round(risk_score, 2),
        }

    @staticmethod
    def _average(values: List[float]) -> float:

        if not values:
            return 0.0

        return sum(values) / len(values)
=======
    def _build_alternative(
        self,
        origin: str,
        destination: str,
        waypoints: Any,
        status: str,
        index: int,
    ) -> Dict[str, Any]:
        adjusted_waypoints = self._adjust_waypoints(waypoints, index)
        risk_modifier = self._estimate_risk_modifier(adjusted_waypoints, status)
        estimated_eta = self._estimate_eta(adjusted_waypoints, index)

        return {
            "origin": origin,
            "destination": destination,
            "status": status,
            "waypoints": adjusted_waypoints,
            "estimated_time_of_arrival": estimated_eta,
            "notes": f"Alternative route option {index}",
            "risk_score": risk_modifier,
            "alternative_index": index,
        }

    def _adjust_waypoints(self, waypoints: Any, index: int) -> Any:
        if isinstance(waypoints, list):
            return waypoints[index - 1 :] + waypoints[: index - 1]
        if isinstance(waypoints, str) and waypoints.strip():
            points = [p.strip() for p in waypoints.split(",")]
            rotated = points[index - 1 :] + points[: index - 1]
            return ", ".join(rotated)
        return waypoints

    def _estimate_risk_modifier(self, waypoints: Any, status: str) -> int:
        modifier = 0
        if status in {"in_progress", "active"}:
            modifier += 10
        if isinstance(waypoints, list):
            modifier += min(len(waypoints) * 2, 20)
        elif isinstance(waypoints, str) and waypoints.strip():
            modifier += min(10, waypoints.count(",") + 1)
        return min(100, modifier + 10)

    def _estimate_eta(self, waypoints: Any, index: int) -> Optional[str]:
        if not waypoints:
            return None
        return f"2026-07-0{index + 1}T08:00:00Z"
from typing import Any, Dict, List, Optional


class RouteAlternatives:
    def generate_alternatives(
        self,
        route: Dict[str, Any],
        count: int = 3,
    ) -> List[Dict[str, Any]]:
        base_origin = route.get("origin", "unknown origin")
        base_destination = route.get("destination", "unknown destination")
        waypoints = route.get("waypoints") or []
        status = route.get("status", "planned")

        alternatives = []
        for idx in range(1, count + 1):
            alternative = self._build_alternative(
                origin=base_origin,
                destination=base_destination,
                waypoints=waypoints,
                status=status,
                index=idx,
            )
            alternatives.append(alternative)

        return alternatives

    def _build_alternative(
        self,
        origin: str,
        destination: str,
        waypoints: Any,
        status: str,
        index: int,
    ) -> Dict[str, Any]:
        adjusted_waypoints = self._adjust_waypoints(waypoints, index)
        risk_modifier = self._estimate_risk_modifier(adjusted_waypoints, status)
        estimated_eta = self._estimate_eta(adjusted_waypoints, index)

        return {
            "origin": origin,
            "destination": destination,
            "status": status,
            "waypoints": adjusted_waypoints,
            "estimated_time_of_arrival": estimated_eta,
            "notes": f"Alternative route option {index}",
            "risk_score": risk_modifier,
            "alternative_index": index,
        }

    def _adjust_waypoints(self, waypoints: Any, index: int) -> Any:
        if isinstance(waypoints, list):
            return waypoints[index - 1 :] + waypoints[: index - 1]
        if isinstance(waypoints, str) and waypoints.strip():
            points = [p.strip() for p in waypoints.split(",")]
            rotated = points[index - 1 :] + points[: index - 1]
            return ", ".join(rotated)
        return waypoints

    def _estimate_risk_modifier(self, waypoints: Any, status: str) -> int:
        modifier = 0
        if status in {"in_progress", "active"}:
            modifier += 10
        if isinstance(waypoints, list):
            modifier += min(len(waypoints) * 2, 20)
        elif isinstance(waypoints, str) and waypoints.strip():
            modifier += min(10, waypoints.count(",") + 1)
        return min(100, modifier + 10)

    def _estimate_eta(self, waypoints: Any, index: int) -> Optional[str]:
        if not waypoints:
            return None
        return f"2026-07-0{index + 1}T08:00:00Z"
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
