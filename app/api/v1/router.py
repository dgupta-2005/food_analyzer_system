from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.meals import router as meals_router
from app.api.v1.packaged_food import router as packaged_food_router
from app.api.v1.collections import router as collections_router
from app.api.v1.recommendations import router as recommendations_router

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(auth_router)
api_v1_router.include_router(meals_router)
api_v1_router.include_router(packaged_food_router)
api_v1_router.include_router(collections_router)
api_v1_router.include_router(recommendations_router)
