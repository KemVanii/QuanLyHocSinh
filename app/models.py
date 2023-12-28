from flask_login import UserMixin
from sqlalchemy import Column, Integer, Double, String, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import db
import enum


class UserRoleEnum(enum.Enum):
    Student = 1
    Teacher = 2
    Employee = 3
    Admin = 4


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    gender = Column(Boolean, nullable=False)
    dob = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRoleEnum))
    score_boards = relationship('Score_board', 'user', lazy=True)
    phones = relationship('Phone', 'user', lazy=True)


class Teacher(User):
    classes = relationship('Class', backref='teacher', lazy=True)


class Khoi(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    classes = relationship('Class', backref='khoi', lazy=True)


class Class(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    size = Column(Integer, nullable=False)
    Khoi_id = Column(Integer, ForeignKey(Khoi.id))
    teacher_id = Column(Integer, ForeignKey(Teacher.id))
    students = relationship('User', backref='class', lazy=True)


class Phone(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))


class Subject(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    score_boards = relationship('Score_board', 'subject', lazy=True)


class Semester(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    # HK1_23
    score_boards = relationship('Score_board', backref='semester', lazy=True)


class ScoreBoard(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    scores = relationship('Score', backref='score_board', lazy=True)
    student_id = Column(Integer, ForeignKey(User.id))
    subject_id = Column(Integer, ForeignKey(Subject.id))
    semester_id = Column(Integer, ForeignKey(Semester.id))


class Score(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Double)
    type = Column(String(20), nullable=False)
    score_board_id = Column(Integer, ForeignKey(ScoreBoard.id))


class Student(User):
    class_id = Column(Integer, ForeignKey(Class.id))
    score_boards_id = Column(Integer, ForeignKey(ScoreBoard.id))


if __name__ == '__main__':
    from app import app

    with app.app_context():
        db.create_all()
    import hashlib

    u = User(name='Admin', username='admin',
             password=str(hashlib.md5('12345'.encode('utf-8')).hexdigest()),
             user_role=UserRoleEnum.Admin)

    db.session.add(u)
    db.session.commit()
