from fastapi import APIRouter
from .auth import endpoint as auth_endpoint
from .completion import endpoint as completion_endpoint
from .courses import endpoint as courses_endpoint
from .enrollment import endpoint as enrollment_endpoint
from .users import endpoint as users_endpoint

api_router = APIRouter()

api_router.include_router(auth_endpoint.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(completion_endpoint.router, prefix="/completion", tags=["Completion"])
api_router.include_router(courses_endpoint.router, prefix="/courses", tags=["Courses"])
api_router.include_router(enrollment_endpoint.router, prefix="/enrollment", tags=["Enrollment"])
api_router.include_router(users_endpoint.router, prefix="/users", tags=["Users"])
