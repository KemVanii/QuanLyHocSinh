from app.models import *
from sqlalchemy import Column, Integer, String, Float, func
from app import db
from app.models import ScoreBoard, Score
import random


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
def getClassByGradeAndSchoolYear(grade, schoolYear):
    classes = (db.session.query(Class)
               .join(Grade)
               .join(ScoreBoard)
               .join(Semester)
               .filter(Grade.name == grade, Semester.name.contains(schoolYear))
               .all())
    return classes


def createNewClassGrade10(className, size, gradeName, currentSchoolYear):
    # Create new Class
    grade_id = db.session.query(Grade).filter(Grade.name == gradeName).first().id
    newClass = Class(name=className, size=size, grade_id=grade_id)
    db.session.add(newClass)
    db.session.commit()
    db.session.refresh(newClass)

    # Create new Score_Boards
    subjects = db.session.query(Subject).all()
    students = getStudentsNotInClass(size)
    semesters = db.session.query(Semester).filter(Semester.name.contains(currentSchoolYear)).all()
    for semester in semesters:
        for subject in subjects:
            for student in students:
                newScoreBoard = ScoreBoard(student_id=student.id, subject_id=subject.id,
                                           class_id=newClass.id, semester_id=semester.id)
                db.session.add(newScoreBoard)

    # Create new TeacherClass
    teachers = db.session.query(User).filter(User.user_role==UserRoleEnum.Teacher).all()
    for subject in subjects:
        filterTeacherBySubject = [teacher for teacher in teachers if teacher.subject_id == subject.id]
        newTeacherClass= TeacherClass(teacher_id=random.choice(filterTeacherBySubject).id,class_id=newClass.id)
        db.session.add(newTeacherClass)
    db.session.commit()

def scores_stats(scoreMin=0, scoreMax=10):
    query = db.session.query(Score.value, func.count(Score.value)).group_by(Score.value)
    if scoreMin:
        query = query.filter(Score.value >= scoreMin)
    if scoreMax:
        query = query.filter(Score.value <= scoreMax)

    return query.all()

    # read json and write json
