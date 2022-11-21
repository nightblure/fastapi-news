from datetime import datetime

from sqlalchemy import (
    Column, String, Integer,
    Boolean, ForeignKey, DateTime,
    sql, Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)


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
    # image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    is_published = Column(Boolean, default=True, nullable=False)
    category = Column(Integer, ForeignKey('categories.id'))  # todo cascade on delete
    views_count = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # uselist=False означает связь 1 к 1. True - один-ко-многим
    user = relationship('User', backref='author', uselist=False)


# реализация связи многие-ко-многим
like = Table(
    'likes', Base.metadata,
    Column('user_id', Integer(), ForeignKey('news.id')),
    Column('news_id', Integer(), ForeignKey('users.id'))
)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True, unique=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='user', uselist=False)

    news_id = Column(Integer, ForeignKey('news.id'), nullable=False)
    news = relationship('News', backref='news', uselist=False)

    text = Column(String)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated = Column(DateTime(timezone=True), onupdate=datetime.now)
