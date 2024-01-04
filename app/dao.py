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

<<<<<<< HEAD

def scores_stats(scoreMin=0, scoreMax=10):
    query = db.session.query(Score.value, func.count(Score.value)).group_by(Score.value)
    if scoreMin:
        query = query.filter(Score.value >= scoreMin)
    if scoreMax:
        query = query.filter(Score.value <= scoreMax)

    return query.all()

=======
def getClassBySchoolYear(schoolYear):
    pass
>>>>>>> 6f0ca50769de617d5f197579ac78c218ad9cff80
# read json and write json
