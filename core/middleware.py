from starlette.middleware.sessions import SessionMiddleware
from fastapi import Request


# @app.middleware("http")
# async def validate_user(request: Request, call_next):
#     print(request.session) # <--- Error: 'AssertionError: SessionMiddleware must be installed to access request.session'
#     response = await call_next(request)
#     return response