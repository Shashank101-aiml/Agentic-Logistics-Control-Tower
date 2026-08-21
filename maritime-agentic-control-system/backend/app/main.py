from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.events import router as event_router
from app.api.routes.risks import router as risk_router
from app.api.routes.workflow import router as workflow_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.recommendation import router as recommendation_router
from app.api.routes.agents import router as agents_router
from app.api.routes.health import router as health_router
<<<<<<< HEAD
from app.api.routes.intelligence import router as intelligence_router
from app.api.routes.vessels import router as vessels_router
=======
from app.api.routes.governance import router as governance_router

from app.database.base import Base
from app.api.dependencies.database import engine, get_db
from app.models.governance import AgentIdentity, AgentHealth

>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
app = FastAPI(
    title="Maritime Agentic Control System",
    description="Backend API for Maritime Agentic AI Control & Route Planning"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
=======
def seed_governance_agents():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    
    agents = [
        {"id": "coordinator-agent", "agent_name": "Coordinator Agent", "agent_type": "ORCHESTRATOR", "version": "v1.0", "risk_level": "MEDIUM", "criticality": "HIGH", "confidence_threshold": 0.8},
        {"id": "ingestion-agent", "agent_name": "Ingestion Agent", "agent_type": "COLLECTOR", "version": "v1.2", "risk_level": "LOW", "criticality": "MEDIUM", "confidence_threshold": 0.5},
        {"id": "risk-agent", "agent_name": "Risk Agent", "agent_type": "ANALYZER", "version": "v2.1", "risk_level": "HIGH", "criticality": "CRITICAL", "confidence_threshold": 0.75},
        {"id": "route-agent", "agent_name": "Route Agent", "agent_type": "PLANNER", "version": "v1.5", "risk_level": "HIGH", "criticality": "CRITICAL", "confidence_threshold": 0.85, "human_approval_required": True},
        {"id": "explanation-agent", "agent_name": "Explanation Agent", "agent_type": "COMMUNICATOR", "version": "v1.0", "risk_level": "LOW", "criticality": "LOW", "confidence_threshold": 0.6}
    ]
    
    for a in agents:
        existing = db.query(AgentIdentity).filter(AgentIdentity.id == a["id"]).first()
        if not existing:
            agent = AgentIdentity(**a)
            db.add(agent)
            db.commit()
            
            health = AgentHealth(agent_id=a["id"], status="HEALTHY")
            db.add(health)
            db.commit()

@app.on_event("startup")
def startup_event():
    seed_governance_agents()

>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
@app.get("/")
def root():
    return {
        "message": "Maritime Agentic Control System Running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

app.include_router(event_router, prefix="/api")
app.include_router(risk_router, prefix="/api")
app.include_router(workflow_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(recommendation_router, prefix="/api")
app.include_router(agents_router, prefix="/api")
app.include_router(health_router, prefix="/api")
<<<<<<< HEAD
app.include_router(intelligence_router, prefix="/api")
app.include_router(vessels_router, prefix="/api")
=======
app.include_router(governance_router, prefix="/api/governance", tags=["governance"])
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
