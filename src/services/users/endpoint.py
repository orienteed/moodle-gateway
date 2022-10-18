from auth.middleware import VerifyTokenRoute
from datetime import datetime
from db.usersDAO import UsersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from logs.setup import logger
from models.users.model import Customer, Customer_update
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


def createCustomer(customer: Customer, customerPassword, request):
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
        + " - Creating user in Moodle..."
    )

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_user_create_users",
        "users[0][username]": customer.username.lower(),
        "users[0][firstname]": customer.firstname,
        "users[0][lastname]": customer.lastname,
        "users[0][email]": customer.username,
        "users[0][password]": customerPassword,
    }

    reply = requests.get("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

    if "exception" in reply.json():
        logger.info(
            "WARNING - ["
            + str(datetime.now())
            + "]: "
            + str(request.client.host)
            + ":"
            + str(request.client.port)
            + " - "
            + str(request.method)
            + " - "
            + str(request.url.path)
            + " - User already exists"
        )
        return getCustomer(customer, request)
    else:
        return reply.json()[0]


def getCustomer(customer: Customer, request):
    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_user_get_users",
        "criteria[0][key]": "username",
        "criteria[0][value]": customer.username,
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
        + " - User created in Moodle successfully"
    )

    return reply.json()["users"][0]


def getCustomerToken(customer: Customer, customerPassword, request):
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
        + " - Fetching customer Moodle token..."
    )

    custom_params = {"username": customer.username.lower(), "password": customerPassword, "service": "pruebas_2"}

    reply = requests.get("{}/login/token.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

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
        + " - Customer Moodle token fetched successfully"
    )

    return reply.json()["token"]


@router.put("/")
def modify_customer(authorization: str = Depends(token_auth_scheme), customer: Customer_update = None, request: Request = None):
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
        + " - Updating customer data in Moodle..."
    )

    user_data = UsersDAO.get_user_data_by_magento_token(request.headers.get("api-authorization"))
    user_id = user_data[0]

    custom_params = {
        "moodlewsrestformat": "json",
        "wstoken": os.getenv("MOODLE_API_KEY_DOCKER"),
        "wsfunction": "core_user_update_users",
        "users[0][id]": user_id,
        "users[0][username]": customer.username.lower(),
        "users[0][email]": customer.username,
    }

    if customer.firstname != "":
        custom_params["users[0][firstname]"] = customer.firstname

    if customer.lastname != "":
        custom_params["users[0][lastname]"] = customer.lastname

    if customer.password is not None:
        custom_params["users[0][password]"] = customer.password

    reply = requests.post("{}/webservice/rest/server.php".format(os.getenv("MOODLE_URL_DOCKER")), params=custom_params)

    if reply.json() == None:
        UsersDAO.update_username_by_id(customer.username, user_id)
        if customer.password:
            newMoodleToken = getCustomerToken(customer, customer.password, request)
            UsersDAO.update_moodle_token_by_id(newMoodleToken, user_id)

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
        + " - Customer data updated in Moodle successfully"
    )

    return JSONResponse({"message": "User modification successfully"})
