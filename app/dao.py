from app.models import *
from sqlalchemy import Column, Integer, String, Float, func
from app import db
from app.models import ScoreBoard, Score


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


def getClassByGradeAndSchoolYear(grade, schoolYear):
    classes = (db.session.query(Class)
               .all())
    print(classes)


def get_semester():
    return  db.session.query(Semester).all()

def get_subject():
    return  db.session.query(Subject).all()

def get_classroom():
    return  db.session.query(Class).all()


def scores_stats(scoreMin=0, scoreMax=10, semester="HK1_23-24", subject="Toán", classroom="10A7"):
    query = db.session.query(func.round(Score.value, 0), func.count(func.round(Score.value, 0))) \
        .join(ScoreBoard, ScoreBoard.id==Score.score_board_id) \
        .join(Semester, Semester.id==ScoreBoard.semester_id) \
        .join(Subject, Subject.id==ScoreBoard.subject_id) \
        .join(Class, Class.id==ScoreBoard.class_id) \
        .group_by(func.round(Score.value, 0)) \
        .order_by(func.round(Score.value, 0).asc())

    if scoreMin:
        query = query.filter(Score.value >= scoreMin)
    if scoreMax:
        query = query.filter(Score.value <= scoreMax)
    if semester:
        query = query.filter(Semester.name.contains(semester))
    if subject:
        query = query.filter(Subject.name.contains(subject))
    if classroom:
        query = query.filter(Class.name.contains(classroom))

    return query.all()


def passed_stats():
    pass


def getClassBySchoolYear(schoolYear):
    pass
# read json and write json
