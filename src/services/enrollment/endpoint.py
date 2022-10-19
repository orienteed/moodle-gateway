from auth.middleware import VerifyTokenRoute
from datetime import datetime
from db.usersDAO import UsersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from logs.setup import logger
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/enroll")
def enroll_user(authorization: str = Depends(token_auth_scheme), courseId: int = None, request: Request = None):
    user_data = UsersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    user_id = user_data[0]

    logger.info(
        "INFO    - ["
        + str(datetime.now())
        + "]: "
        + str(request.client.host)
        + ":"
        + str(request.client.port)
        + " - "
        + str(request.method)
        + " - "
        + str(request.url.path)
        + f" - Enrolling user {user_id} to the course {courseId}..."
    )

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "enrol_manual_enrol_users",
        "enrolments[0][roleid]": 5,  # student
        "enrolments[0][userid]": user_id,
        "enrolments[0][courseid]": courseId,
    }

    requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

    logger.info(
        "INFO    - ["
        + str(datetime.now())
        + "]: "
        + str(request.client.host)
        + ":"
        + str(request.client.port)
        + " - "
        + str(request.method)
        + " - "
        + str(request.url.path)
        + f" - User {user_id} enrolled to the course {courseId} successfully!"
    )

    return JSONResponse({"message": "User enrolled successfully"})


@router.get("/unenroll")
def unenroll_user(authorization: str = Depends(token_auth_scheme), courseId: int = None, request: Request = None):
    user_data = UsersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    user_id = user_data[0]

    logger.info(
        "INFO    - ["
        + str(datetime.now())
        + "]: "
        + str(request.client.host)
        + ":"
        + str(request.client.port)
        + " - "
        + str(request.method)
        + " - "
        + str(request.url.path)
        + f" - Unenrolling user {user_id} from the course {courseId}..."
    )

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "enrol_manual_unenrol_users",
        "enrolments[0][roleid]": 5,  # student
        "enrolments[0][userid]": user_id,
        "enrolments[0][courseid]": courseId,
    }

    requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

    logger.info(
        "INFO    - ["
        + str(datetime.now())
        + "]: "
        + str(request.client.host)
        + ":"
        + str(request.client.port)
        + " - "
        + str(request.method)
        + " - "
        + str(request.url.path)
        + f" - User {user_id} unenrolled from the course {courseId} successfully!"
    )

    return JSONResponse({"message": "User unenrolled successfully"})
