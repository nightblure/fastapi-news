import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import core.auth.router
import news_app.common.views as common_views
import news_app.news.views as news_views
import news_app.categories.views as categories_views
import news_app.auth.views as auth_views
from news_app.models import database

app = FastAPI()

app.mount('/images', StaticFiles(directory='images'), name='images')
app.include_router(common_views.router)
app.include_router(news_views.router)
app.include_router(categories_views.router)
app.include_router(core.auth.router.router)
app.include_router(auth_views.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level='info')
    # uvicorn main:app --reload
