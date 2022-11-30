from fastapi import APIRouter
from sqlalchemy import and_
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from fastapi import Request

# from core.db import session
from news_app.models import Like

router = APIRouter(
    prefix='/news',
)



