from sqlalchemy import Column, Integer, String, BigInteger
from db import Base

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(25), nullable=False)
    