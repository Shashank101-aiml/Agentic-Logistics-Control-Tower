from fastapi import APIRouter

from app.agents.ingestion.ingestion_agent import IngestionAgent
from app.agents.risk.risk_agent import RiskAgent

router = APIRouter()

@router.get("/risks")
def get_risk():

    event = IngestionAgent().collect_data()

    score = RiskAgent().calculate_risk(event)

    return {
        "risk_score": score
    }