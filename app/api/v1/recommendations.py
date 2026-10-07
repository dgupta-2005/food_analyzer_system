from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.db.models.user import UserProfile
from app.db.models.meal import MealLog
from app.schemas.user import UserProfileResponse
from app.schemas.meal import MealLogResponse
from app.schemas.recommendation import MealPlanResponse
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["Meal Plan & Diet Recommendations"])

@router.get("/meal-plan/{user_id}", response_model=MealPlanResponse)
async def generate_personalized_meal_plan(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    """
    UC-4 Service: Analyzes user's historical meal logs, calorie intake, and nutrition habits,
    then generates a customized daily meal/diet plan with target calories and recommended dishes.
    """
    # Fetch User Profile
    profile_stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    profile_res = await db.execute(profile_stmt)
    db_profile = profile_res.scalar_one_or_none()

    if not db_profile:
        # Create default profile DTO
        profile_dto = UserProfileResponse(
            id=0,
            user_id=user_id,
            age=25,
            gender="other",
            weight_kg=70.0,
            height_cm=170.0,
            activity_level="moderately_active",
            primary_goal="maintenance",
            dietary_preference="any",
            target_daily_calories=2000,
            target_protein_g=150,
            target_carbs_g=200,
            target_fat_g=65
        )
    else:
        profile_dto = UserProfileResponse.model_validate(db_profile)

    # Fetch recent meal logs
    logs_stmt = (
        select(MealLog)
        .options(selectinload(MealLog.items))
        .where(MealLog.user_id == user_id)
        .order_by(MealLog.logged_at.desc())
        .limit(30)
    )
    logs_res = await db.execute(logs_stmt)
    db_logs = logs_res.scalars().all()
    recent_log_dtos = [MealLogResponse.model_validate(log) for log in db_logs]

    # Generate plan
    plan = recommendation_service.generate_personalized_plan(profile_dto, recent_log_dtos)
    return plan
