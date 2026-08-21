<<<<<<< HEAD
from datetime import datetime, timedelta, timezone
from math import atan2, cos, radians, sin, sqrt
from typing import Any, Dict, List, Optional

import networkx as nx

from app.agents.route.logistics_graph import LogisticsGraph


class RouteOptimizer:
    """
    Optimizes maritime routes using a NetworkX logistics graph.

    Supports:
    - Dijkstra shortest-path routing
    - A* routing using geographic coordinates
    - Constraint-based route avoidance
    - Distance, cost, delay and risk-aware route weights
    """

    def __init__(self):
        self.logistics_graph = LogisticsGraph()
        self.graph = self.logistics_graph.get_graph()

=======
from typing import Any, Dict, List, Optional


class RouteOptimizer:
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
    def optimize_route(
        self,
        route: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
<<<<<<< HEAD

        constraints = constraints or {}

        origin = route.get("origin")
        destination = route.get("destination")

        # Preserve compatibility with the existing workflow if the
        # incoming route does not map to graph ports.
        if not origin or not destination:
            return self._fallback_response(
                route,
                "Origin or destination was not provided.",
            )

        if origin not in self.graph or destination not in self.graph:
            return self._fallback_response(
                route,
                "Route ports are not available in the logistics graph.",
            )

        graph = self._apply_constraints(constraints)

        if origin not in graph or destination not in graph:
            return self._fallback_response(
                route,
                "Route constraints removed the origin or destination.",
            )

        algorithm = str(
            constraints.get("algorithm", "dijkstra")
        ).lower()

        weight_metric = str(
            constraints.get("weight_metric", "risk")
        ).lower()

        try:
            if algorithm == "astar":
                path = nx.astar_path(
                    graph,
                    origin,
                    destination,
                    heuristic=self._heuristic,
                    weight=lambda u, v, data: self._edge_weight(
                        data,
                        weight_metric,
                    ),
                )
            else:
                path = nx.dijkstra_path(
                    graph,
                    origin,
                    destination,
                    weight=lambda u, v, data: self._edge_weight(
                        data,
                        weight_metric,
                    ),
                )

        except nx.NetworkXNoPath:
            return self._fallback_response(
                route,
                f"No valid path found between {origin} and {destination}.",
            )

        metrics = self._calculate_path_metrics(path)

        eta = self._calculate_eta(
            metrics["total_delay_hours"],
            route.get("departure_time"),
        )

        optimization_score = self._calculate_optimization_score(
            metrics
=======
        constraints = constraints or {}
        waypoints = self._normalize_waypoints(route.get("waypoints"))
        optimized_waypoints = self._apply_constraints(waypoints, constraints)
        route_score = self._score_route(
            origin=route.get("origin"),
            destination=route.get("destination"),
            waypoints=optimized_waypoints,
            status=route.get("status"),
            constraints=constraints,
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
        )

        return {
            **route,
<<<<<<< HEAD
            "origin": origin,
            "destination": destination,
            "waypoints": [
                self._build_waypoint(port)
                for port in path
            ],
            "path": path,
            "optimized": True,
            "algorithm": algorithm,
            "weight_metric": weight_metric,
            "optimization_score": optimization_score,
            "total_distance_nm": metrics["total_distance_nm"],
            "estimated_cost_usd": metrics["estimated_cost_usd"],
            "estimated_delay_hours": metrics["total_delay_hours"],
            "average_weather_severity": metrics[
                "average_weather_severity"
            ],
            "average_congestion_score": metrics[
                "average_congestion_score"
            ],
            "average_incident_score": metrics[
                "average_incident_score"
            ],
            "estimated_time_of_arrival": eta,
            "notes": self._build_notes(
                algorithm,
                weight_metric,
                path,
            ),
        }

    def _apply_constraints(
        self,
        constraints: Dict[str, Any],
    ) -> nx.Graph:

        graph = self.graph.copy()

        avoided_ports = constraints.get(
            "avoid_waypoints",
            [],
        )

        for port in avoided_ports:
            if port in graph:
                graph.remove_node(port)

        return graph

    def _edge_weight(
        self,
        data: Dict[str, Any],
        metric: str,
    ) -> float:

        distance = float(data.get("distance_nm", 0))
        cost = float(data.get("estimated_cost_usd", 0))
        delay = float(data.get("base_delay_hours", 0))

        weather = float(data.get("weather_severity", 0))
        congestion = float(data.get("congestion_score", 0))
        incident = float(data.get("incident_score", 0))

        if metric == "distance":
            return max(distance, 0.001)

        if metric == "cost":
            return max(cost, 0.001)

        if metric == "delay":
            return max(delay, 0.001)

        # Risk-aware composite weight.
        risk_penalty = (
            weather * 0.40
            + congestion * 0.30
            + incident * 0.30
        )

        return (
            distance
            * (1 + risk_penalty)
        )

    def _heuristic(
        self,
        source: str,
        destination: str,
    ) -> float:

        source_data = self.graph.nodes[source]
        destination_data = self.graph.nodes[destination]

        required = {
            "latitude",
            "longitude",
        }

        if not (
            required.issubset(source_data)
            and required.issubset(destination_data)
        ):
            return 0.0

        return self._haversine_distance(
            source_data["latitude"],
            source_data["longitude"],
            destination_data["latitude"],
            destination_data["longitude"],
        )

    def _haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:

        earth_radius_nm = 3440.065

        lat1 = radians(float(lat1))
        lon1 = radians(float(lon1))
        lat2 = radians(float(lat2))
        lon2 = radians(float(lon2))

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(delta_lon / 2) ** 2
        )

        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a),
        )

        return earth_radius_nm * c

    def _calculate_path_metrics(
        self,
        path: List[str],
    ) -> Dict[str, float]:

        total_distance = 0.0
        total_cost = 0.0
        total_delay = 0.0

        weather_scores = []
        congestion_scores = []
        incident_scores = []

        for source, destination in zip(
            path,
            path[1:],
        ):

            edge = self.graph[source][destination]

            total_distance += float(
                edge.get("distance_nm", 0)
            )

            total_cost += float(
                edge.get(
                    "estimated_cost_usd",
                    0,
                )
            )

            total_delay += float(
                edge.get(
                    "base_delay_hours",
                    0,
                )
            )

            weather_scores.append(
                float(
                    edge.get(
                        "weather_severity",
                        0,
                    )
                )
            )

            congestion_scores.append(
                float(
                    edge.get(
                        "congestion_score",
                        0,
                    )
                )
            )

            incident_scores.append(
                float(
                    edge.get(
                        "incident_score",
                        0,
                    )
                )
            )

        edge_count = max(len(path) - 1, 1)

        return {
            "total_distance_nm": round(
                total_distance,
                2,
            ),
            "estimated_cost_usd": round(
                total_cost,
                2,
            ),
            "total_delay_hours": round(
                total_delay,
                2,
            ),
            "average_weather_severity": round(
                sum(weather_scores) / edge_count,
                4,
            ),
            "average_congestion_score": round(
                sum(congestion_scores)
                / edge_count,
                4,
            ),
            "average_incident_score": round(
                sum(incident_scores)
                / edge_count,
                4,
            ),
        }

    def _calculate_optimization_score(
        self,
        metrics: Dict[str, float],
    ) -> float:

        risk = (
            metrics["average_weather_severity"]
            * 40
            + metrics[
                "average_congestion_score"
            ]
            * 30
            + metrics[
                "average_incident_score"
            ]
            * 30
        )

        # Lower risk gives a higher optimization score.
        return round(
            max(0.0, min(100.0, 100.0 - risk)),
            2,
        )

    def _calculate_eta(
        self,
        delay_hours: float,
        departure_time: Optional[str],
    ) -> str:

        if departure_time:
            try:
                departure = datetime.fromisoformat(
                    departure_time.replace(
                        "Z",
                        "+00:00",
                    )
                )
            except ValueError:
                departure = datetime.now(timezone.utc)
        else:
            departure = datetime.now(timezone.utc)

        eta = departure + timedelta(
            hours=delay_hours
        )

        return eta.isoformat()

    def _build_waypoint(
        self,
        port_id: str,
    ) -> Dict[str, Any]:

        port = self.graph.nodes[port_id]

        return {
            "port_id": port_id,
            "label": port.get(
                "port_name",
                port_id,
            ),
            "country": port.get("country"),
            "latitude": port.get("latitude"),
            "longitude": port.get("longitude"),
        }

    def _build_notes(
        self,
        algorithm: str,
        metric: str,
        path: List[str],
    ) -> str:

        return (
            f"Route optimized using "
            f"{algorithm.upper()} with "
            f"{metric}-aware edge weighting. "
            f"Path contains {len(path)} ports."
        )

    def _fallback_response(
        self,
        route: Dict[str, Any],
        reason: str,
    ) -> Dict[str, Any]:

        return {
            **route,
            "optimized": False,
            "optimization_score": None,
            "estimated_time_of_arrival": None,
            "notes": reason,
        }
=======
            "waypoints": optimized_waypoints,
            "optimized": True,
            "optimization_score": route_score,
            "estimated_time_of_arrival": self._estimate_eta(
                optimized_waypoints, route.get("status")
            ),
            "notes": route.get("notes", "") + " Optimized route plan.",
        }

    def _normalize_waypoints(self, waypoints: Any) -> List[Dict[str, Any]]:
        if isinstance(waypoints, list):
            return [self._normalize_waypoint(point) for point in waypoints]
        if isinstance(waypoints, str) and waypoints.strip():
            points = [
                segment.strip() for segment in waypoints.split(",") if segment.strip()
            ]
            return [self._normalize_waypoint(point) for point in points]
        return []

    def _normalize_waypoint(self, waypoint: Any) -> Dict[str, Any]:
        if isinstance(waypoint, dict):
            return waypoint
        if isinstance(waypoint, str):
            return {"label": waypoint}
        return {"label": str(waypoint)}

    def _apply_constraints(
        self, waypoints: List[Dict[str, Any]], constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        if not waypoints:
            return waypoints

        optimized = waypoints.copy()
        if constraints.get("avoid_waypoints"):
            excluded = set(constraints["avoid_waypoints"])
            optimized = [
                waypoint
                for waypoint in optimized
                if waypoint.get("label") not in excluded
            ]

        if constraints.get("preferred_waypoints"):
            preferred = constraints["preferred_waypoints"]
            optimized = sorted(
                optimized,
                key=lambda wp: 0 if wp.get("label") in preferred else 1,
            )

        return optimized

    def _score_route(
        self,
        origin: Optional[str],
        destination: Optional[str],
        waypoints: List[Dict[str, Any]],
        status: Optional[str],
        constraints: Dict[str, Any],
    ) -> float:
        score = 50.0
        if origin and destination:
            score += 10.0
        score += min(len(waypoints) * 5.0, 25.0)

        if status and status.lower() in {"planned", "confirmed"}:
            score += 10.0
        elif status and status.lower() in {"in_progress", "active"}:
            score += 5.0

        if constraints.get("avoid_waypoints"):
            avoided = set(constraints["avoid_waypoints"])
            score -= min(
                15.0,
                sum(1 for wp in waypoints if wp.get("label") in avoided),
            )

        if constraints.get("preferred_waypoints"):
            preferred = set(constraints["preferred_waypoints"])
            score += min(
                15.0,
                sum(1 for wp in waypoints if wp.get("label") in preferred),
            )

        return max(0.0, min(100.0, score))

    def _estimate_eta(
        self, waypoints: List[Dict[str, Any]], status: Optional[str]
    ) -> Optional[str]:
        if not waypoints:
            return None
        base_hours = len(waypoints) * 4
        if status and status.lower() in {"in_progress", "active"}:
            base_hours += 2
        return f"2026-07-0{min(9, base_hours // 24 + 2)}T08:00:00Z"
from typing import Any, Dict, List, Optional


class RouteOptimizer:
    def optimize_route(
        self,
        route: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        constraints = constraints or {}
        waypoints = self._normalize_waypoints(route.get("waypoints"))
        optimized_waypoints = self._apply_constraints(waypoints, constraints)
        route_score = self._score_route(
            origin=route.get("origin"),
            destination=route.get("destination"),
            waypoints=optimized_waypoints,
            status=route.get("status"),
            constraints=constraints,
        )

        return {
            **route,
            "waypoints": optimized_waypoints,
            "optimized": True,
            "optimization_score": route_score,
            "estimated_time_of_arrival": self._estimate_eta(
                optimized_waypoints, route.get("status")
            ),
            "notes": route.get("notes", "") + " Optimized route plan.",
        }

    def _normalize_waypoints(self, waypoints: Any) -> List[Dict[str, Any]]:
        if isinstance(waypoints, list):
            return [self._normalize_waypoint(point) for point in waypoints]
        if isinstance(waypoints, str) and waypoints.strip():
            points = [
                segment.strip() for segment in waypoints.split(",") if segment.strip()
            ]
            return [self._normalize_waypoint(point) for point in points]
        return []

    def _normalize_waypoint(self, waypoint: Any) -> Dict[str, Any]:
        if isinstance(waypoint, dict):
            return waypoint
        if isinstance(waypoint, str):
            return {"label": waypoint}
        return {"label": str(waypoint)}

    def _apply_constraints(
        self, waypoints: List[Dict[str, Any]], constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        if not waypoints:
            return waypoints

        optimized = waypoints.copy()
        if constraints.get("avoid_waypoints"):
            excluded = set(constraints["avoid_waypoints"])
            optimized = [
                waypoint
                for waypoint in optimized
                if waypoint.get("label") not in excluded
            ]

        if constraints.get("preferred_waypoints"):
            preferred = constraints["preferred_waypoints"]
            optimized = sorted(
                optimized,
                key=lambda wp: 0 if wp.get("label") in preferred else 1,
            )

        return optimized

    def _score_route(
        self,
        origin: Optional[str],
        destination: Optional[str],
        waypoints: List[Dict[str, Any]],
        status: Optional[str],
        constraints: Dict[str, Any],
    ) -> float:
        score = 50.0
        if origin and destination:
            score += 10.0
        score += min(len(waypoints) * 5.0, 25.0)

        if status and status.lower() in {"planned", "confirmed"}:
            score += 10.0
        elif status and status.lower() in {"in_progress", "active"}:
            score += 5.0

        if constraints.get("avoid_waypoints"):
            avoided = set(constraints["avoid_waypoints"])
            score -= min(
                15.0,
                sum(1 for wp in waypoints if wp.get("label") in avoided),
            )

        if constraints.get("preferred_waypoints"):
            preferred = set(constraints["preferred_waypoints"])
            score += min(
                15.0,
                sum(1 for wp in waypoints if wp.get("label") in preferred),
            )

        return max(0.0, min(100.0, score))

    def _estimate_eta(
        self, waypoints: List[Dict[str, Any]], status: Optional[str]
    ) -> Optional[str]:
        if not waypoints:
            return None
        base_hours = len(waypoints) * 4
        if status and status.lower() in {"in_progress", "active"}:
            base_hours += 2
        return f"2026-07-0{min(9, base_hours // 24 + 2)}T08:00:00Z"
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
