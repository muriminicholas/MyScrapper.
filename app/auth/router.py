# app/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.auth import utils, schemas, dependencies

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
async def register(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    exists = await db.get(User, user_data.email, options=[])
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = utils.get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name or user_data.email.split("@")[0],
        hashed_password=hashed,
        is_admin=False  # first user as admin optional logic below
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Optional: make first registered user admin
    count = await db.execute("SELECT COUNT(*) FROM users")
    if count.scalar_one() == 1:
        new_user.is_admin = True
        await db.commit()

    return new_user

@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await db.execute("SELECT * FROM users WHERE email = :email", {"email": form_data.username})
    user = user.first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = utils.create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: User = Depends(dependencies.get_current_user)):
    return current_user