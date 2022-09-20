from .graphql.validate_token import magento_validate_token
from datetime import datetime, timedelta
from db.usersDAO import usersDAO
from dotenv import load_dotenv
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from models.users.model import Customer
from starlette.datastructures import MutableHeaders
import json
import os

load_dotenv()


def modify_headers(request: Request, customer: Customer):
    print("Modifying headers...")
    new_header = MutableHeaders(request._headers)
    new_header['customer'] = json.dumps(customer.dict())
    request._headers = new_header
    return request


async def verify_token_db(token):
    print("Verifying token...")
    user_data = usersDAO.get_user_data_by_magento_token(token)
    if user_data is not None:
        last_use_date = user_data[4]
        max_last_use_date = datetime.now() - timedelta(minutes=15)
        last_use_date = datetime.strptime(
            last_use_date, '%Y-%m-%d %H:%M:%S.%f')
        return max_last_use_date > last_use_date
    else:
        return await validate_token(token)


def update_date(token):
    print("Updating last use date...")
    usersDAO.update_token_date(token)


def update_token(username, token):
    print("Updating token...")
    usersDAO.update_user_data(username, token)


async def validate_token(token):
    print("Validating token...")
    transport = AIOHTTPTransport(url=os.getenv(
        'MAGENTO_URL_DOCKER'), headers={'Authorization': f'Bearer {token}'})
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = magento_validate_token()

    try:
        customer_data = await client.execute_async(query)
    except Exception:
        print("ERROR: Invalid token")
        return JSONResponse(content={"message": "Invalid token"}, status_code=401)

    customer_data['customer']['username'] = customer_data['customer'].pop(
        'email')
    customer = Customer(**customer_data['customer'])
    return customer
