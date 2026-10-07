from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.db.models.collection import UserSavedCollection
from app.db.models.product import PackagedProduct
from app.schemas.collection import CollectionSaveRequest, CollectionItemResponse
from app.schemas.product import ProductNutritionSchema

router = APIRouter(prefix="/collections", tags=["User Saved Collections"])

@router.post("/save", response_model=CollectionItemResponse, status_code=status.HTTP_201_CREATED)
async def save_healthy_alternative_to_collection(
    req: CollectionSaveRequest, db: AsyncSession = Depends(get_db)
):
    """
    UC-3 Service: User saves a healthy alternative product to their personal database collection.
    """
    # Verify product exists in database, or create reference
    stmt = select(PackagedProduct).where(PackagedProduct.id == req.product_id)
    res = await db.execute(stmt)
    product = res.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product ID does not exist in backend database.")

    # Check for duplicate
    dup_stmt = select(UserSavedCollection).where(
        UserSavedCollection.user_id == req.user_id,
        UserSavedCollection.product_id == req.product_id
    )
    dup_res = await db.execute(dup_stmt)
    if dup_res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Product is already saved in user collection.")

    entry = UserSavedCollection(
        user_id=req.user_id,
        product_id=req.product_id,
        tag=req.tag,
        user_notes=req.user_notes
    )
    db.add(entry)
    await db.commit()

    fetch_stmt = select(UserSavedCollection).options(selectinload(UserSavedCollection.product)).where(UserSavedCollection.id == entry.id)
    fetched_res = await db.execute(fetch_stmt)
    return fetched_res.scalar_one()

@router.get("/{user_id}", response_model=List[CollectionItemResponse])
async def get_user_collection(
    user_id: int, tag: Optional[str] = None, db: AsyncSession = Depends(get_db)
):
    """UC-3 Retrieval: Fetches saved healthy alternatives collection for a user."""
    query = select(UserSavedCollection).options(selectinload(UserSavedCollection.product)).where(UserSavedCollection.user_id == user_id)
    if tag:
        query = query.where(UserSavedCollection.tag == tag)

    res = await db.execute(query)
    return res.scalars().all()

@router.delete("/{collection_id}", status_code=status.HTTP_200_OK)
async def remove_saved_item(collection_id: int, db: AsyncSession = Depends(get_db)):
    """UC-3 Deletion: Removes an item from user saved collection."""
    stmt = select(UserSavedCollection).where(UserSavedCollection.id == collection_id)
    res = await db.execute(stmt)
    item = res.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Saved collection item not found.")

    await db.delete(item)
    await db.commit()
    return {"message": f"Successfully deleted collection item {collection_id}."}
