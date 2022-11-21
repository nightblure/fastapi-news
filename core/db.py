import os
from core.settings import DATABASE_URL
from sqlmodel import create_engine, SQLModel, Session


engine = create_engine(DATABASE_URL, echo=True)
session = Session(bind=engine)


def init_db():
    SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(bind=engine) as session:
#         yield session
