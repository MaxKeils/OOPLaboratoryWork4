from sqlalchemy.orm import joinedload
from models.course import User
from db import SessionLocal

def add_student(first_name, last_name, email):
    with SessionLocal() as session:
        new_student = User(first_name=first_name, last_name=last_name, email=email)
        session.add(new_student)
        session.commit()
        session.refresh(new_student)
        return new_student

def get_students():
    with SessionLocal() as session:
        return session.query(User).all()

def get_student(student_id):
    with SessionLocal() as session:
        return session.get(User, student_id)

def update_student(student_id, first_name, last_name, email):
    with SessionLocal() as session:
        student = session.get(User, student_id)
        if student:
            student.first_name = first_name
            student.last_name = last_name
            student.email = email
            session.commit()

def delete_student(user_id):
    with SessionLocal() as session:
        student = session.get(User, user_id)
        if student:
            session.delete(student)
            session.commit()
            return True
    return False