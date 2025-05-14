from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from db import Base

from models.user import User


class Course(Base):
    __tablename__ = "course"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'))

    teacher = relationship("User", backref="course")
    