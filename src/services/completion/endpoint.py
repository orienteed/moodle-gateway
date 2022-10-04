from auth.middleware import VerifyTokenRoute
from db.usersDAO import UsersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.security import HTTPBearer
from utils.formatOutput import format_output
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/done")
def mark_as_done(authorization: str = Depends(token_auth_scheme), courseModuleId: int = None, request: Request = None):
    user_data = UsersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    user_id = user_data[0]

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_completion_override_activity_completion_status",
        "cmid": courseModuleId,
        "newstate": 1,  # done
        "userid": user_id,
    }

    reply = requests.post("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

    return format_output(reply.json())
