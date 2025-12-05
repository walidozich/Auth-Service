from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_access_token
from app.crud.user import authenticate_user, create_user, get_user_by_email,get_user_by_username
from app.dependencies import get_current_user, require_admin_user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, Token
from datetime import timedelta
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user_by_email = await get_user_by_email(db, user_in.email)
    user_by_username = await get_user_by_username(db, user_in.username)
    if user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_by_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    return await create_user(db, user_in)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/admin/me", response_model=UserOut)
async def read_admin_me(current_user: User = Depends(require_admin_user)):
    return current_user

@router.get("/get_all_users", response_model=list[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM users")
    users = result.scalars().all()
    return users