from fastapi import APIRouter
from app.agents.coordinator.coordinator_agent import CoordinatorAgent

router = APIRouter()

@router.get("/recommendations")
def get_recommendations():
    result = CoordinatorAgent().run()
    return {
        "status": "SUCCESS",
        "timestamp": "Real-time AI Analysis",
        "action_required": result["risk_score"] > 50,
        "primary_recommendation": result["explanation"],
        "suggested_route": result["route"],
        "assessed_risk": result["risk_score"]
    }
