import aiohttp
from fastapi import Request, Depends, APIRouter, Form, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from aioredis import Redis
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy import and_, select

from core.auth.session import create_session
from core.auth.utils import get_user_by_credentials, get_users_tokens, get_user_tokens
from core.services.redis_ import get_redis_client
from news_app.common.utils import get_auth_route_by_name, get_http_client
from core.auth.users import current_active_user, current_user, password_helper
from core.db import get_async_session
from core.auth.router import router as auth_router
from core.settings import templates
from news_app.models import News, Category, Like, User

router = APIRouter()


@router.get('/login', name='login_route')
async def login_view_get(request: Request):
    context = {
        'request': request
    }
    # x = await get_users_tokens()
    return templates.TemplateResponse('auth/login.html', context=context)


@router.post('/logout', name='logout_route')
async def logout_view(request: Request):
    return RedirectResponse(request.url_for('news_list_route'), status_code=status.HTTP_302_FOUND)


@router.post('/login', name='login_route')
# наименования параметров определяются значениями атрибутов name в HTML-разметке
async def login_view_post(
        request: Request,
        email: str = Form(),
        password: str = Form(),
        http_client: aiohttp.ClientSession = Depends(get_http_client),
        redis: Redis = Depends(get_redis_client)
):
    data = {
        'username': email,
        'password': password
    }

    user = await get_user_by_credentials(email, password)

    if not user:
        return RedirectResponse(request.url_for('login_route'), status_code=status.HTTP_302_FOUND)

    # AUTHORIZE
    auth_url = get_auth_route_by_name(auth_router.routes, 'auth:jwt.login')

    async with http_client.post(url=auth_url, data=data) as response:
        if response.status == 200:
            response_text = await response.json()
            access_token = response_text['access_token']
        else:
            return RedirectResponse(request.url_for('login_route'), status_code=status.HTTP_302_FOUND)

    print(f'SUCCESSFUL LOGIN FOR USER {user.email} ({user.id}), {access_token}')
    response = RedirectResponse(request.url_for('news_list_route'), status_code=status.HTTP_302_FOUND)

    # CREATE SESSION
    await create_session(user.email, response)
    response.set_cookie(key='active_user_email', value=email)

    return response


@router.get('/authenticate', name='auth_route')
async def auth_view(request: Request):
    print(request.headers)
    # url = get_auth_route_by_name(auth_router.routes, 'auth:jwt.login')
    # data = {
    #     'username': request.headers['username'],
    #     'password': request.headers['password']
    # }
    # result = await httpx_client.post(url=url, data=data)
    # access_token = result.json()['access_token']
    # print(access_token)
    return {}


@router.get('/signup', name='signup_route')
async def signup_view(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('auth/signup.html', context=context)
