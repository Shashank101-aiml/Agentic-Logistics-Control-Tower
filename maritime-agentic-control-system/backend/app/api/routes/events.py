from fastapi import APIRouter
from app.agents.ingestion.ingestion_agent import IngestionAgent

router = APIRouter()

@router.get("/events")
def get_events():

    agent = IngestionAgent()

    return agent.collect_data()