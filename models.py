from sqlalchemy import Column, Integer, String
from database import Base


class Register(Base):
    __tablename__ = "User"

    Email_id = Column(String(30), primary_key=True, index=True)
    Name = Column(String(100))
    password = Column(String(225))

class Login(Base):
    __tablename__ = "Login"

    Email_id = Column(String(30), primary_key=True, index=True)
    password = Column(String(225))
    Token = Column(String(500))








