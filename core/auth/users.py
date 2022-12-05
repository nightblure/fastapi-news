# import uuid
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    InvalidPasswordException,
    FastAPIUsers,
    UUIDIDMixin,
    IntegerIDMixin,
)

from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.password import PasswordHelper
from passlib.context import CryptContext

from core.services.redis_ import get_redis_strategy
from news_app.models import User
from core.db import get_user_db  # , User

# почему-то не работает из-за странностей с импортами :С
# from core.services.redis import get_redis_strategy

SECRET = "SECRET"


# class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
class UserManager(IntegerIDMixin, BaseUserManager[User, IntegerIDMixin]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def validate_password(self, password: str, user: User) -> None:
        # if len(password) < 8:
        #     raise InvalidPasswordException(
        #         reason="Password should be at least 8 characters"
        #     )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
password_helper = PasswordHelper(context)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db, password_helper)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    # get_strategy=get_jwt_strategy,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, IntegerIDMixin](get_user_manager, [auth_backend])

# в чем отличие current_user от current_active_user?? протестить во вьюхе
current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
