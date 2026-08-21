from pathlib import Path
from typing import Any, Dict, Optional

import networkx as nx
import pandas as pd


class LogisticsGraph:
    """
    Builds and manages a maritime logistics graph from external
    port and route datasets.

    Nodes represent ports and edges represent available maritime routes.
    Route attributes are loaded dynamically from maritime_routes.csv.
    """

    REQUIRED_PORT_COLUMNS = {
        "port_id",
        "port_name",
        "country",
        "latitude",
        "longitude",
    }

    REQUIRED_ROUTE_COLUMNS = {
        "route_id",
        "source_port",
        "destination_port",
        "distance_nm",
        "estimated_cost_usd",
        "base_delay_hours",
        "weather_severity",
        "congestion_score",
        "incident_score",
    }

    def __init__(
        self,
        ports_path: Optional[Path] = None,
        routes_path: Optional[Path] = None,
    ):
        project_dir = Path(__file__).resolve().parents[4]

        self.ports_path = ports_path or (
            project_dir / "data" / "raw" / "ports.csv"
        )

        self.routes_path = routes_path or (
            project_dir / "data" / "raw" / "maritime_routes.csv"
        )

        self.graph = nx.Graph()

    def build_graph(self) -> nx.Graph:
        """
        Load datasets, validate them, and construct the logistics graph.
        """

        ports_df = self._load_csv(
            self.ports_path,
            "ports dataset",
        )

        routes_df = self._load_csv(
            self.routes_path,
            "maritime routes dataset",
        )

        self._validate_columns(
            ports_df,
            self.REQUIRED_PORT_COLUMNS,
            "ports dataset",
        )

        self._validate_columns(
            routes_df,
            self.REQUIRED_ROUTE_COLUMNS,
            "maritime routes dataset",
        )

        self._add_ports(ports_df)
        self._add_routes(routes_df)

        return self.graph

    def _load_csv(
        self,
        path: Path,
        dataset_name: str,
    ) -> pd.DataFrame:

        if not path.exists():
            raise FileNotFoundError(
                f"{dataset_name.capitalize()} not found: {path}"
            )

        try:
            return pd.read_csv(path)
        except Exception as exc:
            raise ValueError(
                f"Failed to load {dataset_name}: {exc}"
            ) from exc

    def _validate_columns(
        self,
        dataframe: pd.DataFrame,
        required_columns: set,
        dataset_name: str,
    ) -> None:

        missing_columns = required_columns - set(dataframe.columns)

        if missing_columns:
            raise ValueError(
                f"{dataset_name.capitalize()} is missing "
                f"required columns: {sorted(missing_columns)}"
            )

    def _add_ports(
        self,
        ports_df: pd.DataFrame,
    ) -> None:

        for _, port in ports_df.iterrows():

            port_id = str(port["port_id"]).strip()

            if not port_id:
                continue

            attributes: Dict[str, Any] = {
                column: port[column]
                for column in ports_df.columns
                if column != "port_id"
            }

            self.graph.add_node(
                port_id,
                **attributes,
            )

    def _add_routes(
        self,
        routes_df: pd.DataFrame,
    ) -> None:

        available_ports = set(self.graph.nodes)

        for _, route in routes_df.iterrows():

            source = str(route["source_port"]).strip()
            destination = str(route["destination_port"]).strip()

            if source not in available_ports:
                raise ValueError(
                    f"Route references unknown source port: {source}"
                )

            if destination not in available_ports:
                raise ValueError(
                    f"Route references unknown destination port: {destination}"
                )

            route_attributes = {
                column: route[column]
                for column in routes_df.columns
                if column not in {
                    "source_port",
                    "destination_port",
                }
            }

            self.graph.add_edge(
                source,
                destination,
                **route_attributes,
            )

    def get_graph(self) -> nx.Graph:
        """
        Return the current graph.

        Builds the graph automatically if it has not been built yet.
        """

        if self.graph.number_of_nodes() == 0:
            self.build_graph()

        return self.graph

    def get_port(self, port_id: str) -> Dict[str, Any]:
        """
        Return metadata for a specific port.
        """

        graph = self.get_graph()

        if port_id not in graph:
            raise ValueError(f"Unknown port: {port_id}")

        return dict(graph.nodes[port_id])

    def get_route(
        self,
        source_port: str,
        destination_port: str,
    ) -> Dict[str, Any]:
        """
        Return attributes for a direct maritime route.
        """

        graph = self.get_graph()

        if not graph.has_edge(source_port, destination_port):
            raise ValueError(
                f"No direct route between "
                f"{source_port} and {destination_port}"
            )

        return dict(
            graph[source_port][destination_port]
        )

    def summary(self) -> Dict[str, int]:
        """
        Return basic graph statistics.
        """

        graph = self.get_graph()

        return {
            "ports": graph.number_of_nodes(),
            "routes": graph.number_of_edges(),
        }