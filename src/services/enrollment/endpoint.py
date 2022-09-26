from auth.middleware import VerifyTokenRoute
from db.usersDAO import usersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/enroll")
def enroll_user(authorization: str = Depends(token_auth_scheme), courseId: int = None, request: Request = None):
    user_data = usersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    user_id = user_data[0]

    customParams = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "enrol_manual_enrol_users",
        "enrolments[0][roleid]": 5,  # student
        "enrolments[0][userid]": user_id,
        "enrolments[0][courseid]": courseId,
    }

    reply = requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=customParams)

    return JSONResponse({"message": "User enrolled successfully"})


@router.get("/unenroll")
def unenroll_user(authorization: str = Depends(token_auth_scheme), courseId: int = None, request: Request = None):
    user_data = usersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    user_id = user_data[0]

    customParams = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "enrol_manual_unenrol_users",
        "enrolments[0][roleid]": 5,  # student
        "enrolments[0][userid]": user_id,
        "enrolments[0][courseid]": courseId,
    }

    reply = requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=customParams)

    return JSONResponse({"message": "User unenrolled successfully"})

