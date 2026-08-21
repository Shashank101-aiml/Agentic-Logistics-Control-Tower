from typing import Any, Dict, Optional

from app.agents.ingestion.ingestion_agent import IngestionAgent
from app.agents.risk.risk_agent import RiskAgent
from app.agents.route.route_agent import RouteAgent
from app.agents.explanation.explanation_agent import ExplanationAgent


class CoordinatorAgent:
    """
    Coordinates the complete maritime intelligence workflow.

    Pipeline:
    Event Ingestion
        -> ML Risk Assessment
        -> Route Optimization
        -> Alternative Route Ranking
        -> AI Explanation
    """

    def __init__(self) -> None:
        self.ingestion_agent = IngestionAgent()
        self.risk_agent = RiskAgent()
        self.route_agent = RouteAgent()
        self.explanation_agent = ExplanationAgent()

    def run(
        self,
        source_payload: Optional[Dict[str, Any]] = None,
        route_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        # 1. Collect and normalize incoming event data
        event = self.ingestion_agent.collect_data(
            source_payload
        )

        # 2. Calculate ML-based operational risk
        risk = self.risk_agent.calculate_risk(
            event=event,
            route=route_context,
        )

        # 3. Generate and rank optimized route alternatives
        route_decision = self.route_agent.suggest_route(
            risk_score=risk,
            current_route=route_context,
        )

        # 4. Generate explanation
        explanation = self.explanation_agent.explain(
            route=route_decision,
            event=event,
            risk=risk,
            recommendations=route_decision.get(
                "alternatives",
                [],
            ),
        )

        return {
            "event": event,
            "risk_assessment": risk,
            "route_decision": route_decision,
            "explanation": explanation,
        }