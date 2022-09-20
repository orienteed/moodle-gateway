from ..users.endpoint import createCustomer, getCustomer, getCustomerToken
from auth.middleware import VerifyTokenRoute
from db.usersDAO import usersDAO
from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from models.users.model import Customer
import json

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.post('/login')
async def login(authorization: str = Depends(token_auth_scheme), request: Request = None):
    requestData = await request.json()
    customer = json.loads(request.headers["customer"])
    customer = Customer(**customer)

    magento_token = request.headers.get("api-authorization")
    username = customer.username

    user = usersDAO.get_user_data_by_username(username)
    if user is None:
        customerId = createCustomer(customer, requestData['password'])['id']
    else:
        customerId = user[0]

    moodle_token = getCustomerToken(
        customer, requestData['password'])

    usersDAO.create_and_update_user(
        customerId, username, magento_token, moodle_token)

    return JSONResponse({"message": "Login successfully"})


@ router.post('/logout')
async def logout(authorization: str = Depends(token_auth_scheme), request: Request = None):
    token = request.headers.get("api-authorization")
    usersDAO.remove_token_by_token(token)
    return JSONResponse({"message": "Logout successfully"})
