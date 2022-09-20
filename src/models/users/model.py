from pydantic import BaseModel, EmailStr
from typing import Optional


class Customer(BaseModel):
    username: EmailStr
    firstname: str
    lastname: str


class Customer_update(BaseModel):
    username: Optional[EmailStr]
    firstname: Optional[str]
    lastname: Optional[str]
    password: Optional[str]
