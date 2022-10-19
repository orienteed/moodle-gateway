from ..users.endpoint import createCustomer, getCustomerToken
from auth.middleware import VerifyTokenRoute
from datetime import datetime
from db.usersDAO import UsersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from logs.setup import logger
from models.users.model import Customer
import json

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.post("/login")
async def login(authorization: str = Depends(token_auth_scheme), request: Request = None):
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
        + " - Doing loging..."
    )
    requestData = await request.json()
    customer = json.loads(request.headers["customer"])
    customer = Customer(**customer)

    magento_token = request.headers.get("api-authorization")
    username = customer.username

    user = UsersDAO.get_user_data_by_username(username)
    if user is None:
        customerId = createCustomer(customer, requestData["password"], request)["id"]

    else:
        customerId = user[0]

    try:
        moodle_token = getCustomerToken(customer, requestData["password"], request)
    except:
        moodle_token = ""
        logger.info(
            "ERROR   - ["
            + str(datetime.now())
            + "]: "
            + str(request.client.host)
            + ":"
            + str(request.client.port)
            + " - "
            + str(request.method)
            + " - "
            + str(request.url.path)
            + " - Error generating moodle token"
        )

    UsersDAO.create_and_update_user(customerId, username, magento_token, moodle_token)
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
        + " - New user created successfully"
    )
    return JSONResponse({"message": "Login successfully"})


@router.post("/logout")
async def logout(authorization: str = Depends(token_auth_scheme), request: Request = None):
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
        + " - Doing logout..."
    )
    token = request.headers.get("api-authorization")
    UsersDAO.remove_token_by_token(token)
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
        + " - User logged out successfully"
    )
    return JSONResponse({"message": "Logout successfully"})
