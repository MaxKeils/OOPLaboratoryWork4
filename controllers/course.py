from sqlalchemy.orm import joinedload
from models.course import Course
from db import SessionLocal


def add_course(title, author_id):
    """Добавить новый курс."""
    with SessionLocal() as session:
        new_course = Course(title=title, author_id=author_id)
        session.add(new_course)
        session.commit()
        session.refresh(new_course)
        return new_course


def get_courses():
    """Получить список всех курсов."""
    with SessionLocal() as session:
        return session.query(Course).all()


def get_course(course_id):
    """Получить курс по ID."""
    with SessionLocal() as session:
        return session.get(Course, course_id)


def update_course(course_id, title, author_id):
    """Обновить информацию о курсе."""
    with SessionLocal() as session:
        course = session.get(Course, course_id)
        if course:
            course.title = title
            course.author_id = author_id
            session.commit()
            session.refresh(course)
            return course
        return None


def delete_course(course_id):
    """Удалить курс по ID."""
    with SessionLocal() as session:
        course = session.get(Course, course_id)
        if course:
            session.delete(course)
            session.commit()
            return True
        return False