from typing import Callable

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

import core.auth.router
import news_app.auth.views as auth_views
import news_app.categories.views as categories_views
import news_app.common.views as common_views
import news_app.news.views as news_views
from core.auth.session import session_router
from news_app.models import database

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

app.mount('/images', StaticFiles(directory='images'), name='images')

app.include_router(common_views.router)
app.include_router(news_views.router)
app.include_router(categories_views.router)
app.include_router(core.auth.router.router)
app.include_router(auth_views.router)
app.include_router(session_router)


@app.middleware("http")
async def validate_user(
        request: Request,
        call_next: Callable,
):
    """
    Создаем кастомное свойство session и записываем туда данные текущей сессии
    Свойство request.state предназначено для хранения любой дополнительной информации
        согласно документации starlette

    https://github.com/tiangolo/fastapi/issues/4746
    """
    # DONT WORK
    # request.state.session = session_data
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level='info')
    # RUM FROM TERMINAL: uvicorn main:app --reload
