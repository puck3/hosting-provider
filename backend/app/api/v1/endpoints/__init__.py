from fastapi import APIRouter
from . import hardwares
from . import plans
from . import rentals
from . import servers
from . import users
from . import auth

router = APIRouter()

router.include_router(hardwares.router)
router.include_router(plans.router)
router.include_router(rentals.router)
router.include_router(servers.router)
router.include_router(users.router)
router.include_router(auth.router)
