from fastapi import APIRouter
from . import hardwares
from . import plans
from . import rentals
from . import servers
from . import users

router = APIRouter(tags=["API v1"])

router.include_router(hardwares.router)
router.include_router(plans.router)
router.include_router(rentals.router)
router.include_router(servers.router)
router.include_router(users.router)
