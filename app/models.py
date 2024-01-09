from flask_login import UserMixin
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import app, db
import enum


class UserRoleEnum(enum.Enum):
    Teacher = 1
    Employee = 2
    Admin = 3

    def __str__(self):
        return self.name


class Student(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(Boolean, nullable=False)
    dob = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    phones = relationship('PhoneStudent', foreign_keys='PhoneStudent.student_id', backref='student', lazy=True)
    email = Column(String(50), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    score_boards = relationship('ScoreBoard', foreign_keys='ScoreBoard.student_id', backref='student', lazy=True)


class Subject(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    score_boards = relationship('ScoreBoard', backref='subject', lazy=True)
    classes = relationship('User', foreign_keys='User.subject_id', backref='subject', lazy=True)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(Boolean, nullable=False)
    dob = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRoleEnum))
    status = Column(Boolean, default=True, nullable=False)
    phones = relationship('PhoneUser', foreign_keys='PhoneUser.user_id', backref='user', lazy=True)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=True)

    def __str__(self):
        return self.name


class Grade(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    classes = relationship('Class', backref='grade', lazy=True)


class Class(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    size = Column(Integer, nullable=False)
    grade_id = Column(Integer, ForeignKey(Grade.id), nullable=False)
    score_boards = relationship('ScoreBoard', foreign_keys='ScoreBoard.class_id', backref='class', lazy=True)


class PhoneUser(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)

class PhoneStudent(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(10), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=True)


class Semester(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    # HK1_23-24
    score_boards = relationship('ScoreBoard', backref='semester', lazy=True)


class ScoreBoard(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    scores = relationship('Score', backref='score_board', lazy=True)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    status = Column(Boolean, default=True, nullable=False)


class Score(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float)
    type = Column(String(20), nullable=False)
    score_board_id = Column(Integer, ForeignKey(ScoreBoard.id))


class TeacherClass(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey(User.id))
    class_id = Column(Integer, ForeignKey(Class.id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        #
        # u = User(name='Nguyễn Văn Admin', username='admin', gender=True, dob='1991-01-01', address='TPHCM',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.Admin, status=True, subject_id=1)
        # #
        # db.session.add(u)
        # db.session.commit()
        # u = User(name='Nguyễn Văn NhanVien', username='nhanVien', gender=True, dob='1991-01-01', address='TPHCM',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.Employee)
        #
        # db.session.add(u)
        # db.session.commit()
        # u = User(name='Nguyễn Văn GiaoVien', username='giaoVien', gender=True, dob='1991-01-01', address='TPHCM',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.Teacher)
        #
        # db.session.add(u)
        # db.session.commit()
