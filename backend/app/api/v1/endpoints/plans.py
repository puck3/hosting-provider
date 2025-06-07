from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.v1.schemas.plan import CreatePlan
from app.dependencies.actor import Actor, get_actor
from app.dependencies.services_factory import get_services_factory
from app.models.plan import Plan
from app.models.user import Role
from app.services.factory import ServicesFactory

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/")
async def get_plans(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> list[Plan]:
    plan_service = services.get_plan_service()
    return plan_service.get_plans()


@router.get("/available/{country}")
async def get_available_plans_by_country(
    country: str,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> list[Plan]:
    try:
        plan_service = services.get_plan_service()
        return await plan_service.get_available_plans_by_country(country)
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/")
async def add_plan(
    plan: CreatePlan,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> Plan:
    if actor.role != Role.admin:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail="Only admin can create plan.",
        )
    try:
        plan_service = services.get_plan_service()
        return plan_service.add_plan(**plan.model_dump())
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    if actor.role != Role.admin:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail="Only admin can create plan.",
        )
    try:
        plan_service = services.get_plan_service()
        plan_service.delete_plan(plan_id)
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e)) from e
