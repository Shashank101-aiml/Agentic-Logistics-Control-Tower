from fastapi import FastAPI
app = FastAPI(
    title="Maritime Agentic Control System",
)
@app.get("/")
def root():
    return{
        "message": "Maritime Agentic Control System Running"
    }
@app.get("/health")
def health():
    return{
        "status": "healthy"
    }
from app.api.routes.events import router as event_router
app.include_router(event_router)
