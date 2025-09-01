from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.models import Users

router = APIRouter(
    prefix="/users",
)

@router.get("/{telegram_id}")
async def get_user(telegram_id: int,
                   session: AsyncSession = Depends(get_async_session)):
    user = (await session.execute(
        select(
            Users
        ).where(Users.telegram_id == telegram_id)
    )).scalar()
    if user:
        return user
    raise HTTPException(
        status_code=404
    )

@router.delete("/{telegram_id}")
async def get_user(telegram_id: int,
                   session: AsyncSession = Depends(get_async_session)):
    user = (await session.execute(
        select(
            Users
        ).where(Users.telegram_id == telegram_id)
    )).scalar()
    if user:
        await session.delete(user)
        await session.commit()
    raise HTTPException(
        status_code=404
    )


