from auth.middleware import VerifyTokenRoute
from db.usersDAO import UsersDAO
from fastapi import APIRouter, Depends, Response
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/course")
def get_media_course(authorization: str = Depends(token_auth_scheme), uri: str = None, request: Request = None):
    custom_params = {"token": os.getenv("MOODLE_API_KEY_DOCKER")}

    reply = requests.get(f'{os.getenv("MOODLE_URL_DOCKER")}/{uri}', params=custom_params)

    try:
        headers = {"media_type": reply.headers["Content-Type"]}
        return Response(content=reply.content, headers=headers)
    except:
        return JSONResponse({"error": "Media not found"})


@router.get("/resource")
def get_media_resource(authorization: str = Depends(token_auth_scheme), uri: str = None, request: Request = None):
    user_data = UsersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    moodle_token = user_data[3]

    custom_params = {"token": moodle_token}

    reply = requests.get(f'{os.getenv("MOODLE_URL_DOCKER")}/{uri}', params=custom_params)

    try:
        headers = {"media_type": reply.headers["Content-Type"]}
        return Response(content=reply.content, headers=headers)
    except:
        return JSONResponse({"error": "Media not found"})
