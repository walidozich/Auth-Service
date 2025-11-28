from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed = get_password_hash(user_in.password)
    db_user = User(email=user_in.email, username=user_in.username, hashed_password=hashed)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def update_user(db: AsyncSession, user_id: int, user_in: UserCreate):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    user.email = user_in.email
    user.username = user_in.username
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    await db.delete(user)
    await db.commit()
    return user