from typing import Any, Union

import aiohttp
from aioredis import Redis
from fastapi import Request, Depends, APIRouter, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from core.auth.utils import get_user_tokens, get_user_by_email
from core.services.redis_ import get_redis_client

from news_app.common.utils import get_http_client
from core.auth.users import current_active_user, current_user
from core.db import get_async_session

from core.settings import templates
from news_app.models import News, Category, Like, User

router = APIRouter(
    prefix="/news",
)


async def get_news_list_context(session: AsyncSession = Depends(get_async_session)) -> dict[str, Any]:
    # подгружаем поле из relationship - likes
    news = await session.execute(select(News).options(selectinload(News.likes)))
    news = news.scalars().all()

    # подгружаем поле из relationship - news_list
    categories = await session.execute(select(Category).options(selectinload(Category.news_list)))
    categories = categories.scalars().all()

    categories_info = {category.title: len(category.news_list) for category in categories}

    # region вариант сбора информации о лайках с помощью запроса к БД
    # likes_info_query = session.query(
    #     Like.news_id,
    #     func.count(Like.news_id).label('likes_count')
    # ).group_by(Like.news_id).all()

    # likes_info = {info_obj.news_id: info_obj.likes_count for info_obj in likes_info_query}
    # endregion

    news_likes_count = {news_item.id: len(news_item.likes) for news_item in news}
    await session.commit()
    context = {
        'news': news,
        'categories_info': categories_info,
        'news_likes_count': news_likes_count,
    }
    return context


@router.get('/', name='news_list_route')
async def news_list_view(
        request: Request,
        http_client: aiohttp.ClientSession = Depends(get_http_client),
        redis: Redis = Depends(get_redis_client),
        # user: User = Depends(current_active_user),
        context: dict[str, Any] = Depends(get_news_list_context),
):
    active_user_email = request.cookies.get('active_user_email')

    if active_user_email:
        user = await get_user_by_email(active_user_email)
        # users_tokens: list = await get_user_tokens(active_user_email, redis)
        context['user'] = user

    context['request'] = request
    return templates.TemplateResponse('news_list.html', context=context)
    # return response


# @router.get('/news_auth', name='news_auth_list_route')
# async def news_auth_view(
#         request: Request,
#         context: dict[str, Any] = Depends(get_news_list_context),
#         user: User = Depends(current_active_user)
# ):
#     context['user'] = user
#     context['request'] = request
#     return templates.TemplateResponse('news_list.html', context=context)


@router.post('like/{news_id}', name='news_like_route')
async def like_view(request: Request, news_id: int, session: AsyncSession = Depends(get_async_session)):
    filtered = await session.execute(select(Like).filter(and_(Like.news_id == news_id, Like.user_id == 1)))
    filtered = filtered.scalars().first()

    if filtered:
        await session.delete(filtered)
    else:
        like_obj = Like(user_id=1, news_id=news_id)
        session.add(like_obj)

    await session.commit()
    return RedirectResponse(request.url_for('news_list_route'), status_code=status.HTTP_302_FOUND)


@router.post('create_news', name='create_news_route')
async def v(request: Request):
    return RedirectResponse(request.url_for('news_route'), status_code=status.HTTP_302_FOUND)
