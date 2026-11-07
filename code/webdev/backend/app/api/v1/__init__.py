from fastapi import APIRouter
from app.api.v1 import inspections, lots, dashboard

api_v1_router = APIRouter()

api_v1_router.include_router(inspections.router, prefix="/inspections", tags=["Inspections"])
api_v1_router.include_router(lots.router, prefix="/lots", tags=["Lots"])
api_v1_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])