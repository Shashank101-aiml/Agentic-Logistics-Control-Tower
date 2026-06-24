from app.agents.ingestion.ingestion_agent import IngestionAgent
from app.agents.risk.risk_agent import RiskAgent
from app.agents.route.route_agent import RouteAgent
from app.agents.explanation.explanation_agent import ExplanationAgent

class CoordinatorAgent:

    def run(self):

        event = IngestionAgent().collect_data()

        risk = RiskAgent().calculate_risk(event)

        route = RouteAgent().suggest_route(risk)

        explanation = ExplanationAgent().explain(route)

        return {
            "event": event,
            "risk_score": risk,
            "route": route,
            "explanation": explanation
        }