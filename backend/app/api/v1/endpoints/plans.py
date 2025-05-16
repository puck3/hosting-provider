from fastapi import APIRouter, Depends

from app.api.v1.schemas.plan import CreatePlan
from app.services.factory import ServicesFactory
from app.dependencies.services_factory import get_services_factory
from app.models.plan import Plan

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/")
async def get_plans(
    services: ServicesFactory = Depends(get_services_factory),
) -> list[Plan]:
    plan_service = services.get_plan_service()
    return plan_service.get_plans()


@router.get("/available/{country}")
async def get_available_plans_by_country(
    country: str,
    services: ServicesFactory = Depends(get_services_factory),
) -> list[Plan]:
    plan_service = services.get_plan_service()
    return plan_service.get_available_plans_by_country(country)


@router.post("/")
async def add_plan(
    plan: CreatePlan,
    services: ServicesFactory = Depends(get_services_factory),
) -> Plan:
    plan_service = services.get_plan_service()
    return plan_service.add_plan(**plan.model_dump())


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    services: ServicesFactory = Depends(get_services_factory),
) -> None:
    plan_service = services.get_plan_service()
    plan_service.delete_plan(plan_id)
