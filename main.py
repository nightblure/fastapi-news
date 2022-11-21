import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from core.db import session
from news_app.models import News, Category
from core.settings import DATABASE_URL

import databases

app = FastAPI()

templates = Jinja2Templates(directory="templates")
database = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def news_list(request: Request):

    news = session.query(News).all()
    categories = session.query(Category).all()
    print(news)
    print(categories)
    context = {
        'request': request,
        'news': news,
        'categories': categories,
    }
    return templates.TemplateResponse('news_list.html', context=context)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
# uvicorn main:app --reload
