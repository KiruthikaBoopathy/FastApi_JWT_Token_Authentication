from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    Email_id: str = Field(max_length=30)
    Name: str = Field(max_length=100)
    password: str = Field(max_length=225)


class User_login(BaseModel):
    Email_id: str = Field(max_length=30)
    password: str = Field(max_length=225)


class LogoutRequest(BaseModel):
    email_id: str
