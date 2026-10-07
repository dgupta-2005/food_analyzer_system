from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.db.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserResponse, UserProfileCreate, UserProfileResponse
from app.core.security import get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication & User Profiles"])

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginSuccessResponse(BaseModel):
    message: str
    user: UserResponse

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registers a new user with secure PBKDF2 password hashing and default profile."""
    stmt = select(User).where(User.email == user_in.email)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    hashed_pw = get_password_hash(user_in.password)

    new_user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        full_name=user_in.full_name
    )
    db.add(new_user)
    await db.flush()

    # Create default user profile
    default_profile = UserProfile(user_id=new_user.id)
    db.add(default_profile)
    await db.commit()

    # Fetch fresh user with profile loaded
    stmt = select(User).options(selectinload(User.profile)).where(User.id == new_user.id)
    res = await db.execute(stmt)
    return res.scalar_one()

@router.post("/login", response_model=LoginSuccessResponse)
async def login_user(login_in: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticates user with email and password."""
    stmt = select(User).options(selectinload(User.profile)).where(User.email == login_in.email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return LoginSuccessResponse(
        message="Login successful.",
        user=UserResponse.model_validate(user)
    )

@router.put("/profile/{user_id}", response_model=UserProfileResponse)
async def update_profile(user_id: int, profile_in: UserProfileCreate, db: AsyncSession = Depends(get_db)):
    """Updates user nutritional goals and physical profile attributes."""
    stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    res = await db.execute(stmt)
    profile = res.scalar_one_or_none()

    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)

    for field, val in profile_in.model_dump(exclude_unset=True).items():
        setattr(profile, field, val)

    await db.commit()
    await db.refresh(profile)
    return profile
