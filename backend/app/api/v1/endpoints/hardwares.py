from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.v1.schemas.hardware import CreateCPU, CreateGPU, CreateHardware
from app.dependencies.actor import Actor, get_actor
from app.dependencies.services_factory import get_services_factory
from app.models.user import Role
from app.services.factory import ServicesFactory
from app.models.hardware import CPU, GPU, Hardware

router = APIRouter(prefix="/hardwares", tags=["Hardwares"])


@router.get("/")
async def get_hardwares(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> list[Hardware]:
    try:
        hw_service = services.get_hardware_service()
        return hw_service.get_hardwares()
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/")
async def create_hardware(
    hw: CreateHardware,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> Hardware:
    if actor.role != Role.admin:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only admin can create hardware.",
        )
    try:
        hw_service = services.get_hardware_service()
        return hw_service.create_hardware(**hw.model_dump())
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{hardware_id}")
async def delete_hardware(
    hardware_id: int,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
    actor: Annotated[Actor, Depends(get_actor)],
):
    if actor.role != Role.admin:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only admin can create hardware.",
        )
    try:
        hw_service = services.get_hardware_service()
        hw_service.delete_hardware(hardware_id)
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/cpus")
async def get_cpus(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> list[CPU]:
    try:
        hw_service = services.get_hardware_service()
        return hw_service.get_cpus()
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/cpus")
async def add_cpu(
    cpu: CreateCPU,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> CPU:
    if actor.role != Role.admin:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only admin can create hardware.",
        )
    try:
        hw_service = services.get_hardware_service()
        return hw_service.add_cpu(**cpu.model_dump())
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/cpus/{cpu_id}")
async def delete_cpu(
    cpu_id: int,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> None:
    if actor.role != Role.admin:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only admin can create hardware.",
        )
    try:
        hw_service = services.get_hardware_service()
        hw_service.delete_cpu(cpu_id)
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/gpus")
async def get_gpus(
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
) -> list[GPU]:
    try:
        hw_service = services.get_hardware_service()
        return hw_service.get_gpus()
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/gpus")
async def add_gpu(
    gpu: CreateGPU,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
    actor: Annotated[Actor, Depends(get_actor)],
) -> GPU:
    if actor.role != Role.admin:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only admin can create hardware.",
        )
    try:
        hw_service = services.get_hardware_service()
        return hw_service.add_gpu(**gpu.model_dump())
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/gpus/{gpu_id}")
async def delete_gpu(
    gpu_id: int,
    services: Annotated[ServicesFactory, Depends(get_services_factory)],
    actor: Annotated[Actor, Depends(get_actor)],
):
    if actor.role != Role.admin:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only admin can create hardware.",
        )
    try:
        hw_service = services.get_hardware_service()
        hw_service.delete_gpu(gpu_id)
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=str(e))
