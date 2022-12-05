from aioredis import Redis
from sqlalchemy import select

from core.auth.users import password_helper
from core.db import async_session
from news_app.models import User


async def get_user_tokens(email: str, redis: Redis) -> list:
    user: User = await get_user_by_email(email)

    if not user:
        return []

    users_tokens: dict = await get_users_tokens(redis)
    tokens = []

    for token in users_tokens:
        user_id = users_tokens.get(token)
        if user_id == str(user.id):
            tokens.append(token)

    return tokens


async def get_users_tokens(redis: Redis, pattern: str = 'fastapi_users_token*') -> dict:
    users_tokens = await redis.keys(pattern=pattern)
    result = {}

    for token in users_tokens:
        user_id = await redis.get(token)
        result[token.replace(f'{pattern}:', '')] = user_id
        # print(f'token: {token}; user_id: {user_id}')

    return result


async def get_user_by_email(email: str) -> User:
    async with async_session() as session:
        user = await session.execute(
            select(User)
            .filter(User.email == email)
        )

    user = user.scalars().first()
    return user


# return object from User model or None
async def get_user_by_credentials(email: str, password: str) -> User | None:
    user: User = await get_user_by_email(email)

    if not user:
        return None
        # raise Exception(f"user with email '{email}' does not exists")

    is_correct_credentials = password_helper.verify_and_update(
        plain_password=password,
        hashed_password=user.hashed_password)[0]

    return user if is_correct_credentials else None
