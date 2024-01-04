from app.models import *
from sqlalchemy import Column, Integer, String
from app import db


def load_function(user_role):
    if user_role == UserRoleEnum.Employee:
        return [
            {

                'name': 'Tiếp nhận học sinh',
                'url': '/student'
            },
            {
                'name': 'Lập danh sách',
                'url': '/lapdanhsach'
            },
            {
                'name': 'Điều chỉnh danh sách',
                'url': '/dieuchinhdanhsach'
            },
        ]
    elif user_role == UserRoleEnum.Teacher:
        return [

            {
                'url': '/menu',
                'name': 'Nhập Điểm',
                'url': '/nhapdiem'
            },
            {
                'name': 'Chỉnh sửa Điểm',
                'url': '/chinhsuadiem'
            },
            {
                'name': 'Xem Điểm',
                'url': '/xemdiem'
            }
        ]
    elif user_role == UserRoleEnum.Admin:
        return [
            {
                'name': 'Quy định',
                'url': '/quydinh'
            },
            {
                'name': 'Thống kê',
                'url': '/thongke'
            }
        ]
    return []


def getStudentsNotInClass(limit):
    students_with_score_boards = (db.session.query(Student)
                                  .filter(Student.score_boards == None)
                                  .limit(limit).all())

    return students_with_score_boards


def getClassBySchoolYear(schoolYear):
    pass


# read json and write json

def getScoreBoard(tenLop, tenMon, hocKi):
    score_boards = (db.session.query(ScoreBoard)
               .join(Class)
               .join(Subject)
               .join(Semester)
               # .filter(Semester.name.contains(schoolYear)).all())
               .filter(Class.name == tenLop, Subject.name == tenMon, Semester.name == hocKi).all())
    return score_boards
