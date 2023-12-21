import datetime
from credentials import credentials
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from starlette import status
import models
import schemas
from fastapi import FastAPI, HTTPException, Depends
from Auth import hash_pass
from models import Register, Login
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import bcrypt
from fastapi.openapi.models import Info
from Auth import hash_pass, authenticate_user, create_access_token, decode_token
from fastapi.openapi.models import Info, Tag

app = FastAPI()


def my_schema():
    openapi_schema = get_openapi(
        title="The Amazing Programming Language Info API",
        version="1.0",
        routes=app.routes,
    )
    openapi_schema["info"] = {
        "title": "The Amazing Programming Language Info API",
        "version": "1.0",
        "description": "Learn about programming language history!",
        "termsOfService": "http://programming-languages.com/terms/",
        "contact": {
            "name": "Get Help with this API",
            "url": "http://www.programming-languages.com/help",
            "email": "support@programming-languages.com"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
        },
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = my_schema

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/Register', tags=["Registration"])
def create_users(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_pass = hash_pass(user.password)
    user.password = hashed_pass
    new_user = models.Register(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post('/Login_token', tags=["Login"])
def login_for_access_token(form_data: schemas.User_login, db: Session = Depends(get_db)):
    user = authenticate_user(form_data.Email_id, form_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials", )

    access_token_expires = datetime.timedelta(days=365000)
    access_token = create_access_token(data={"sub": user.Email_id}, expires_delta=access_token_expires)
    login_info = Login(Email_id=user.Email_id, password=user.password, Token=access_token)
    db.add(login_info)
    db.commit()
    return {"token_type": "bearer", "access_token": access_token}


@app.post('/Protection_check', tags=["Login"])
def protected_route(decoded_token: dict = Depends(decode_token)):
    return {"message": "This is a protected route", "decoded_token": decoded_token}


@app.post('/Logout', tags=["Logout"])
def logout(logout_request: schemas.LogoutRequest, db: Session = Depends(get_db)):
    user_email = logout_request.email_id
    login_info = db.query(Login).filter(Login.Email_id == user_email).first()
    if login_info:
        db.delete(login_info)
        db.commit()

    return {"message": "Logout successful"}
