from fastapi import Depends, APIRouter

# from core.db import UserInDb
from core.auth.schemas import UserCreate, UserRead, UserUpdate
from core.auth.users import auth_backend, current_active_user, fastapi_users
from news_app.models import User
# from core.db import User

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

for r in router.routes:
    print(r)
