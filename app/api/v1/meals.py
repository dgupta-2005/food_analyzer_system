from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.db.models.meal import MealLog, MealItem
from app.schemas.meal import (
    MealEstimationResponse,
    MealLogCreate,
    MealLogResponse,
    MacroNutrientItem
)
from app.services.storage_service import storage_service
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/meals", tags=["Meal Calorie Estimation & Logging"])

@router.post("/estimate", response_model=MealEstimationResponse)
async def estimate_meal_calories(
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """
    UC-1 Service: Upload an image or provide text description of daily meals.
    Returns estimated calorie count, portion breakdown, and macro breakdown using AI.
    """
    if not description and not image:
        raise HTTPException(
            status_code=400, detail="Provide at least a text meal description or an image file."
        )

    saved_image_url = None
    saved_local_path = None

    if image:
        # Save image via StorageService (Firebase / Local)
        saved_image_url = await storage_service.save_file(image, subfolder="meals")
        # For Gemini vision API, convert relative URL to local disk path if stored locally
        if saved_image_url.startswith("/uploads/"):
            saved_local_path = saved_image_url.replace("/uploads/", str(storage_service.upload_dir) + "/")

    try:
        estimation = gemini_service.estimate_meal(
            image_path=saved_local_path,
            description=description
        )

        return MealEstimationResponse(
            summary_item_name=estimation.summary_item_name,
            total_calories=estimation.total_calories,
            total_protein_g=estimation.total_protein_g,
            total_carbs_g=estimation.total_carbs_g,
            total_fats_g=estimation.total_fats_g,
            confidence_score=estimation.confidence_score,
            image_url=saved_image_url,
            items=estimation.items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Meal estimation failed: {str(e)}")

@router.post("/log", response_model=MealLogResponse, status_code=status.HTTP_201_CREATED)
async def log_meal(meal_in: MealLogCreate, db: AsyncSession = Depends(get_db)):
    """Persists estimated meal into database for user history."""
    log_entry = MealLog(
        user_id=meal_in.user_id,
        image_url=meal_in.image_url,
        user_description=meal_in.user_description,
        total_calories=meal_in.total_calories,
        total_protein_g=meal_in.total_protein_g,
        total_carbs_g=meal_in.total_carbs_g,
        total_fats_g=meal_in.total_fats_g,
    )
    db.add(log_entry)
    await db.flush()

    for item in meal_in.items:
        db_item = MealItem(
            meal_log_id=log_entry.id,
            item_name=item.item_name,
            portion_description=item.portion_description,
            calories=item.calories,
            protein_g=item.protein_g,
            carbs_g=item.carbs_g,
            fats_g=item.fats_g,
            confidence_score=item.confidence_score,
        )
        db.add(db_item)

    await db.commit()

    stmt = select(MealLog).options(selectinload(MealLog.items)).where(MealLog.id == log_entry.id)
    res = await db.execute(stmt)
    return res.scalar_one()

@router.get("/history/{user_id}", response_model=List[MealLogResponse])
async def get_user_meal_history(user_id: int, db: AsyncSession = Depends(get_db)):
    """Fetches full log history of user daily meals."""
    stmt = (
        select(MealLog)
        .options(selectinload(MealLog.items))
        .where(MealLog.user_id == user_id)
        .order_by(MealLog.logged_at.desc())
    )
    res = await db.execute(stmt)
    return res.scalars().all()
