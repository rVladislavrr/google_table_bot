from fastapi import APIRouter

from . import routers

router = APIRouter(prefix="/v1")

router.include_router(routers.users)
router.include_router(routers.utils)