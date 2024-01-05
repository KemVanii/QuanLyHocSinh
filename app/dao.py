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
            },
            {
                'name': 'Tài khoản',
                'url': '/user'
            },
            {
                'name': 'Môn học',
                'url': '/subject'
            },


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

def getScoreBoard(tenLop, subjectName, hocKi):
    score_boards = (db.session.query(ScoreBoard.id, Student.name, Student.dob)
                    .join(Class)
                    .join(Subject)
                    .join(Semester)
                    .join(Student)
                    .filter(Class.name == tenLop, Subject.name == subjectName, Semester.name == hocKi).all())
    return score_boards


def getClassByGradeAndSchoolYear(grade, schoolYear):
    classes = (db.session.query(Class)
               .join(Grade)
               .join(ScoreBoard)
               .join(Semester)
               .filter(Grade.name == grade, Semester.name.contains(schoolYear))
               .all())
    print(classes)
    return classes


def getAllSubject():
    return db.session.query(Subject).all()


def createNewClassGrade10(className, size, gradeName, currentSchoolYear):
    # Create new Class
    grade_id = db.session.query(Grade).filter(Grade.name == gradeName).first().id
    newClass = Class(name=className, size=size, grade_id=grade_id)
    db.session.add(newClass)
    db.session.commit()
    db.session.refresh(newClass)

    # Create new Score_Boards
    subjects = getAllSubject()
    students = getStudentsNotInClass(size)
    semesters = db.session.query(Semester).filter(Semester.name.contains(currentSchoolYear)).all()
    for semester in semesters:
        for subject in subjects:
            for student in students:
                newScoreBoard = ScoreBoard(student_id=student.id, subject_id=subject.id,
                                           class_id=newClass.id, semester_id=semester.id)
                db.session.add(newScoreBoard)

    # Create new TeacherClass
    teachers = db.session.query(User).filter(User.user_role == UserRoleEnum.Teacher).all()
    for subject in subjects:
        filterTeacherBySubject = [teacher for teacher in teachers if teacher.subject_id == subject.id]
        newTeacherClass = TeacherClass(teacher_id=random.choice(filterTeacherBySubject).id, class_id=newClass.id)
        db.session.add(newTeacherClass)
    db.session.commit()


def get_semester():
    return db.session.query(Semester).all()


def get_subject():
    return db.session.query(Subject).all()


def get_classroom():
    return db.session.query(Class).all()


def scores_stats(scoreMin=0, scoreMax=10, semester="HK1_23-24", subject="Toán", classroom="10A7"):
    query = db.session.query(func.round(Score.value, 0), func.count(func.round(Score.value, 0))) \
        .join(ScoreBoard, ScoreBoard.id == Score.score_board_id) \
        .join(Semester, Semester.id == ScoreBoard.semester_id) \
        .join(Subject, Subject.id == ScoreBoard.subject_id) \
        .join(Class, Class.id == ScoreBoard.class_id) \
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


def insert_score(dataScores):
    for dataScore in dataScores:
        for i in range(len(dataScore['15p'])):
            s = Score(value=dataScore['15p'][i], type='15p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        for i in range(len(dataScore['45p'])):
            s = Score(value=dataScore['45p'][i], type='15p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        s = Score(value=dataScore['ck'], type='ck', score_board_id=dataScore['score_board_id'])
        db.session.add(s)
        db.session.commit()

# read json and write json
