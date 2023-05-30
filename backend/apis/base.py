from fastapi import APIRouter
from apis.version1.route_users import user_router
from apis.version1.route_login import login_router
from apis.version1.route_question import question_router
from apis.version1.route_answers import answer_router

base_router = APIRouter()

#we include all routers here and include only base_router in main -> just preventing messing up main.py
base_router.include_router(user_router, prefix="/users", tags=["users"])
base_router.include_router(login_router, prefix="/login", tags=["login"])
base_router.include_router(question_router, prefix="/question", tags=["questions"])
base_router.include_router(answer_router, prefix="/answers", tags=["answers"])