from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from db import Base


class Enrollment(Base):
    __tablename__ = "enrollment"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, ForeignKey('course.id', ondelete='CASCADE'))
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'))

    course = relationship("Course", backref="enrollment")
    user = relationship("User", backref="enrollment")