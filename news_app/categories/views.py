from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import and_
from starlette import status

from core.db import get_async_session
from core.settings import templates
from news_app.models import News, Category, Like

router = APIRouter(
    prefix="/cats",
)

session = get_async_session()

@router.post('create_category', response_class=HTMLResponse, name='create_category_route')
async def v(request: Request):
    pass


@router.post('create_category', response_class=HTMLResponse, name='token_route')
async def v(request: Request):
    pass


@router.post('create_category', response_class=HTMLResponse, name='jwt_token_route')
async def v(request: Request):
    pass



@router.post('create_category', response_class=HTMLResponse, name='logout_route')
async def v(request: Request):
    pass

@router.post('create_category', response_class=HTMLResponse, name='edit_profile_route')
async def v(request: Request):
    pass

