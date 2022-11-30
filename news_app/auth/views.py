import httpx
from fastapi import Request, Depends, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from news_app.common.utils import get_auth_route_by_name
from core.auth.users import current_active_user, current_user
from core.db import get_async_session


from core.auth.router import router as auth_router
from core.settings import templates
from news_app.models import News, Category, Like, User

router = APIRouter()


@router.get('/login', name='login_route')
async def login_view(request: Request):
    context = {
        'request': request
    }
    return templates.TemplateResponse('auth/login.html', context=context)


@router.post('/login', name='login_route')
# наименования параметров определяются значениями атрибутов name в HTML-разметке
async def login_view(request: Request, email: str = Form(), password: str = Form()):

    url = get_auth_route_by_name(auth_router.routes, 'auth:jwt.login')
    print(url)

    data = {
        'username': email,
        'password': password
    }

    # TODO async post query
    async with httpx.AsyncClient() as client:
        result = await client.post(url=url, data=data)
        print(result.is_success)

    if result.is_success:
        context = {

        }
        return RedirectResponse(request.url_for('news_list_route'), status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(request.url_for('login_route'), status_code=status.HTTP_302_FOUND)


@router.get('/signup', name='signup_route')
async def signup_view(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('auth/signup.html', context=context)
