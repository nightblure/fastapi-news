from typing import AsyncGenerator

import databases
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.settings import DATABASE_URL, DEBUG
from news_app.models import User

if DEBUG:
    engine = create_async_engine(DATABASE_URL, echo=True)
else:
    engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


# class User(SQLAlchemyBaseUserTableUUID, Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True, index=True, unique=True)
#     # email = Column(String, unique=True)
#     # is_admin = Column(Boolean, default=False)
#     # hashed_password = Column(String)
#     # likes = relationship('Like', uselist=True)
#     # путь к аватарке. нужна таблица путей к картинкам аватаров пользователей



async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
