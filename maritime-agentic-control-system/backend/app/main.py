from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.events import router as event_router
from app.api.routes.risks import router as risk_router
from app.api.routes.workflow import router as workflow_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.recommendation import router as recommendation_router
from app.api.routes.agents import router as agents_router
from app.api.routes.health import router as health_router

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
