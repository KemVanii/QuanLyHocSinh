from flask_login import UserMixin
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import app, db
import enum


class UserRoleEnum(enum.Enum):
    Teacher = 1
    Employee = 2
    Admin = 3


class Person(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    gender = Column(Boolean, nullable=False)
    dob = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    phones = relationship('Phone', foreign_keys='Phone.person_id',backref='person', lazy=True)
    user = relationship('User', foreign_keys='User.person_id', backref='person', lazy=True)
    classes = relationship('Class', foreign_keys='Class.teacher_id', backref='user', lazy=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRoleEnum))
    person_id = Column(Integer, ForeignKey(Person.id))


class Khoi(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    classes = relationship('Class', backref='khoi', lazy=True)


class Class(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    size = Column(Integer, nullable=False)
    Khoi_id = Column(Integer, ForeignKey(Khoi.id), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    students = relationship('Student', foreign_keys='Student.class_id', backref='class', lazy=True)


class Phone(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(10), nullable=False)
    person_id = Column(Integer, ForeignKey(Person.id), nullable=False)


class Subject(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    score_boards = relationship('ScoreBoard', backref='subject', lazy=True)


class Semester(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    # HK1_23
    score_boards = relationship('ScoreBoard', backref='semester', lazy=True)


class ScoreBoard(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    scores = relationship('Score', backref='score_board', lazy=True)
    student_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)


class Student(Person):
    class_id = Column(Integer, ForeignKey(Class.id))
    score_boards = relationship('ScoreBoard', backref='student', lazy=True)


class Score(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float)
    type = Column(String(20), nullable=False)
    score_board_id = Column(Integer, ForeignKey(ScoreBoard.id))


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        import hashlib

        u = User(name='Admin', username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.Admin)

        db.session.add(u)
        db.session.commit()
