from datetime import datetime

import databases
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import (
    Column, String, Integer,
    Boolean, ForeignKey, DateTime,
    sql
)
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from core.settings import DATABASE_URL

database = databases.Database(DATABASE_URL)
Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    # email = Column(String, unique=True)
    # is_admin = Column(Boolean, default=False)
    # hashed_password = Column(String)
    # likes = relationship('Like', uselist=True)
    # путь к аватарке. нужна таблица путей к картинкам аватаров пользователей


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String, unique=True)
    slug = Column(String, unique=True)


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String(150))
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)
    # image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True) # todo imagefield
    is_published = Column(Boolean, default=True, nullable=False)

    category_id = Column(Integer, ForeignKey('categories.id'))  # todo cascade on delete

    """ uselist=False означает связь 1 к 1. True - один-ко-многим
    в модели Category неявно создастся атрибут news_list, 
    по которому будут доступны все новости: category.news_list,
    а в модели News останется атрибут category """
    category = relationship('Category', backref='news_list', uselist=False, lazy='subquery')

    views_count = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User', backref='news_list', uselist=False, lazy='subquery')

    likes = relationship('Like', uselist=True, lazy='subquery')
    # путь к картинке. нужна таблица путей к картинкам новостей


class Like(Base):
    __tablename__ = 'likes'
    __table_args__ = (
        UniqueConstraint('user_id', 'news_id'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    news_id = Column(Integer, ForeignKey('news.id'))


# реализация связи многие-ко-многим
class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True, unique=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User', backref='comments', uselist=True, lazy='subquery')

    news_id = Column(Integer, ForeignKey('news.id'), nullable=False)
    news = relationship('News', backref='comments_list', uselist=True, lazy='subquery')

    text = Column(String)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated = Column(DateTime(timezone=True), onupdate=datetime.now)
