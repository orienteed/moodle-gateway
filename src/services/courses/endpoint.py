from auth.middleware import VerifyTokenRoute
from datetime import datetime
from db.usersDAO import UsersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.security import HTTPBearer
from logs.setup import logger
from utils.formatOutput import format_output
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/")
def get_courses(authorization: str = Depends(token_auth_scheme), request: Request = None):
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
        + " - Fetching courses..."
    )

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_course_get_courses_by_field",
    }

    reply = requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

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
        + " - Courses fetched successfully"
    )

    return format_output(reply.json())


@router.get("/details")
def get_course_details(authorization: str = Depends(token_auth_scheme), id: int = None, request: Request = None):
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
        + f" - Fetching course {id} details..."
    )

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_course_get_courses_by_field",
        "field": "id",
        "value": id,
    }

    reply = requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

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
        + f" - Course details {id} fetched successfully"
    )

    return format_output(reply.json())


@router.get("/content")
def get_course_content(authorization: str = Depends(token_auth_scheme), id: int = None, enrolled: str = "false", request: Request = None):
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
        + f" - Fetching course {id} content..."
    )

    user_data = UsersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    moodle_token = user_data[3]

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": moodle_token if enrolled == "true" else os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_course_get_contents",
        "courseid": id,
    }

    reply = requests.post("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

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
        + f" - Course {id} content fetched successfully"
    )

    return format_output(reply.json())


@router.get("/progress")
def get_course_progress(authorization: str = Depends(token_auth_scheme), request: Request = None):
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
        + " - Fetching user courses in progress..."
    )

    user_data = UsersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    user_id = user_data[0]
    moodle_token = user_data[3]

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": moodle_token,
        "wsfunction": "core_enrol_get_users_courses",
        "userid": user_id,
    }

    reply = requests.post("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

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
        + " - User courses in progress fetched successfully"
    )

    return format_output(reply.json())


@router.get("/category")
def get_courses_by_category(authorization: str = Depends(token_auth_scheme), categoryId: int = None, request: Request = None):
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
        + f" - Fetching courses from category {categoryId}..."
    )

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_course_get_courses_by_field",
        "field": "category",
        "value": categoryId,
    }

    reply = requests.post("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

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
        + f" - Courses from category {categoryId} fetched successfully"
    )

    return format_output(reply.json())
