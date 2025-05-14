from models.enrollment import Enrollment
from db import SessionLocal


def add_enrollment(course_id, user_id):
    """Добавить запись о зачислении пользователя на курс."""
    with SessionLocal() as session:
        new_enrollment = Enrollment(course_id=course_id, user_id=user_id)
        session.add(new_enrollment)
        session.commit()
        session.refresh(new_enrollment)
        return new_enrollment


def get_enrollments():
    """Получить список всех зачислений."""
    with SessionLocal() as session:
        return session.query(Enrollment).all()


def get_enrollment(enrollment_id):
    """Получить запись о зачислении по ID."""
    with SessionLocal() as session:
        return session.get(Enrollment, enrollment_id)


def get_enrollments_by_course(course_id):
    """Получить список зачислений для конкретного курса."""
    with SessionLocal() as session:
        return session.query(Enrollment).filter_by(course_id=course_id).all()


def get_enrollments_by_user(user_id):
    """Получить список зачислений для конкретного пользователя."""
    with SessionLocal() as session:
        return session.query(Enrollment).filter_by(user_id=user_id).all()


def delete_enrollment(enrollment_id):
    """Удалить запись о зачислении по ID."""
    with SessionLocal() as session:
        enrollment = session.get(Enrollment, enrollment_id)
        if enrollment:
            session.delete(enrollment)
            session.commit()
            return True
        return False