from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents.coordinator.coordinator_agent import CoordinatorAgent


router = APIRouter(
    prefix="/intelligence",
    tags=["Maritime Intelligence"],
)


class MaritimeIntelligenceRequest(BaseModel):

    event: Dict[str, Any] = Field(
        ...,
        description="Operational event data",
    )

    route: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Current route context",
    )


@router.post("/analyze")
def analyze_maritime_operation(
    request: MaritimeIntelligenceRequest,
):

    try:

        coordinator = CoordinatorAgent()

        result = coordinator.run(
            source_payload=request.event,
            route_context=request.route,
        )

        return {
            "status": "success",
            "system": "Maritime Agentic Control System",
            "result": result,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Maritime intelligence analysis failed",
                "error": str(error),
            },
        )