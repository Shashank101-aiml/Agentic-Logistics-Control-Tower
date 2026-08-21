<<<<<<< HEAD
from fastapi import APIRouter

from app.agents.coordinator.coordinator_agent import CoordinatorAgent

router = APIRouter()

@router.get("/run-workflow")
def run_workflow():

    return CoordinatorAgent().run()
=======
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.agents.coordinator.coordinator_agent import CoordinatorAgent

router = APIRouter()

@router.get("/run-workflow")
def run_workflow(session_id: str = None, db: Session = Depends(get_db)):
    return CoordinatorAgent().run(db=db, session_id=session_id)
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
