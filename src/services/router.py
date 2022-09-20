from fastapi import APIRouter
from .auth import endpoint as auth_endpoint
from .users import endpoint as users_endpoint

api_router = APIRouter()

api_router.include_router(auth_endpoint.router, prefix='/auth', tags=["Authentication"])
api_router.include_router(users_endpoint.router, prefix='/users', tags=["Users"])