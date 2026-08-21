from fastapi import APIRouter

from app.agents.coordinator.coordinator_agent import CoordinatorAgent

router = APIRouter()

@router.get("/run-workflow")
def run_workflow():

    return CoordinatorAgent().run()