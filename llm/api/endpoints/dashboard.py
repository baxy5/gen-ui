from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.dashboard_service import DashboardService
from schemas.dashboard_schema import RequestSchema, ResponseSchema


router = APIRouter()


@router.post("/generate")
async def generate(
    request: RequestSchema, service: Annotated[DashboardService, Depends()]
) -> ResponseSchema:

    try:
        return await service.generate_dashboard(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate dashboard: {e}",
        )
