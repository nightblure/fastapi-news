from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from core.auth.users import current_active_user, current_user
from core.db import get_async_session

from core.settings import templates
from news_app.models import News, Category, Like, User

router = APIRouter(
    prefix="/news",
)

# current_user: User = Depends(current_user),
#                     current_active_user: User = Depends(current_active_user)


@router.get('/', response_class=HTMLResponse, name='news_list_route')
async def news_list(request: Request, session: AsyncSession = Depends(get_async_session)):
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
        'request': request,
        'news': news,
        'categories_info': categories_info,
        'news_likes_count': news_likes_count,
    }
    print(current_user)
    print(current_active_user)
    return templates.TemplateResponse('news_list.html', context=context)


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
