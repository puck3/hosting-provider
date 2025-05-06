from fastapi import APIRouter, Depends

from app.api.v1.schemas.hardware import CreateCPU, CreateGPU, CreateHardware
from app.db.connector import ServicesFactory, get_services_factory
from app.models.hardware import CPU, GPU, Hardware

router = APIRouter(prefix="/hardwares", tags=["Hardwares"])


@router.get("/")
async def get_hardwares(
    services: ServicesFactory = Depends(get_services_factory),
) -> list[Hardware]:
    hw_service = services.get_hardware_service()
    return hw_service.get_hardwares()


@router.post("/")
async def create_hardware(
    hw: CreateHardware,
    services: ServicesFactory = Depends(get_services_factory),
) -> Hardware:
    hw_service = services.get_hardware_service()
    return hw_service.create_hardware(**hw.model_dump())


@router.delete("/{hardware_id}")
async def delete_hardware(
    hardware_id: int,
    services: ServicesFactory = Depends(get_services_factory),
) -> None:
    hw_service = services.get_hardware_service()
    hw_service.delete_hardware(hardware_id)


@router.get("/cpus")
async def get_cpus(
    services: ServicesFactory = Depends(get_services_factory),
) -> list[CPU]:
    hw_service = services.get_hardware_service()
    return hw_service.get_cpus()


@router.post("/cpus")
async def add_cpu(
    cpu: CreateCPU,
    services: ServicesFactory = Depends(get_services_factory),
) -> CPU:
    hw_service = services.get_hardware_service()
    return hw_service.add_cpu(**cpu.model_dump())


@router.delete("/cpus/{cpu_id}")
async def delete_cpu(
    cpu_id: int,
    services: ServicesFactory = Depends(get_services_factory),
) -> None:
    hw_service = services.get_hardware_service()
    hw_service.delete_cpu(cpu_id)


@router.get("/gpus")
async def get_gpus(
    services: ServicesFactory = Depends(get_services_factory),
) -> list[GPU]:
    hw_service = services.get_hardware_service()
    return hw_service.get_gpus()


@router.post("/gpus")
async def add_gpu(
    gpu: CreateGPU,
    services: ServicesFactory = Depends(get_services_factory),
) -> GPU:
    hw_service = services.get_hardware_service()
    return hw_service.add_gpu(**gpu.model_dump())


@router.delete("/gpus/{gpu_id}")
async def delete_gpu(
    gpu_id: int,
    services: ServicesFactory = Depends(get_services_factory),
) -> None:
    hw_service = services.get_hardware_service()
    hw_service.delete_gpu(gpu_id)
