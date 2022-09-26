from auth.middleware import VerifyTokenRoute
from db.usersDAO import usersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from models.users.model import Customer, Customer_update
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


def createCustomer(customer: Customer, customerPassword):
    customParams = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_user_create_users",
        "users[0][username]": customer.username.lower(),
        "users[0][firstname]": customer.firstname,
        "users[0][lastname]": customer.lastname,
        "users[0][email]": customer.username,
        "users[0][password]": customerPassword,
    }

    reply = requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=customParams)

    if "exception" in reply.json():
        return getCustomer(customer)
    else:
        return reply.json()[0]


def getCustomer(customer: Customer):
    customParams = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_user_get_users",
        "criteria[0][key]": "username",
        "criteria[0][value]": customer.username,
    }

    reply = requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=customParams)

    return reply.json()["users"][0]


def getCustomerToken(customer: Customer, customerPassword):
    customParams = {"username": customer.username.lower(), "password": customerPassword, "service": "pruebas_2"}

    reply = requests.get("{}/login/token.php".format(os.getenv("MOODLE_URL_DOCKER")), params=customParams)

    return reply.json()["token"]


@router.put("/")
def modify_customer(authorization: str = Depends(token_auth_scheme), customer: Customer_update = None, request: Request = None):
    user_data = usersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    user_id = user_data[0]

    customParams = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_user_update_users",
        "users[0][id]": user_id,
        "users[0][username]": customer.username.lower(),
        "users[0][email]": customer.username,
    }

    if customer.firstname != "":
        customParams["users[0][firstname]"] = customer.firstname

    if customer.lastname != "":
        customParams["users[0][lastname]"] = customer.lastname

    if customer.password is not None:
        customParams["users[0][password]"] = customer.password

    reply = requests.post("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=customParams)

    if reply.json() == None:
        usersDAO.update_username_by_id(customer.username, user_id)
        if customer.password:
            newMoodleToken = getCustomerToken(customer, customer.password)
            usersDAO.update_moodle_token_by_id(newMoodleToken, user_id)

    return JSONResponse({"message": "User modification successfully"})
