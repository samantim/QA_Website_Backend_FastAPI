from fastapi import APIRouter
from apis.version1.route_users import user_router
from apis.version1.route_login import login_router

base_router = APIRouter()

base_router.include_router(user_router, prefix="/users", tags=["users"])
base_router.include_router(login_router, prefix="/login", tags=["login"])