from app.models import *
from sqlalchemy import Column, Integer, String, Float, func, desc, asc
from app import db
from app.models import ScoreBoard, Score
import random


def load_function(user_role):
    if user_role == UserRoleEnum.Employee:
        return [
            {
                'name': 'Tiếp nhận học sinh',
                'endpoint': 'student'
            },
            {
                'name': 'Lập danh sách',
                'endpoint': 'lapdanhsach'
            },
            {
                'name': 'Điều chỉnh danh sách',
                'endpoint': 'dieuchinhdanhsach'
            },
        ]
    elif user_role == UserRoleEnum.Teacher:
        return [

            {
                'name': 'Nhập Điểm',
                'endpoint': 'nhapdiem'
            },
            {
                'name': 'Chỉnh sửa Điểm',
                'endpoint': 'chinhsuadiem'
            },
            {
                'name': 'Xem Điểm',
                'endpoint': 'xemdiem'
            }
        ]
    elif user_role == UserRoleEnum.Admin:
        return [
            {
                'name': 'Quy định',
                'endpoint': 'quydinh'
            },
            {
                'name': 'Thống kê',
                'endpoint': 'thongke'
            },
            {
                'name': 'Tài khoản',
                'endpoint': 'user'
            },
            {
                'name': 'Môn học',
                'endpoint': 'subject'
            },

        ]
    return []


def getStudentsNotInClass(limit):
    students_with_score_boards = (db.session.query(Student)
                                  .filter(Student.score_boards == None)
                                  .limit(limit).all())

    return students_with_score_boards


# read json and write json

def getScoreBoard(className, subjectName, semester, currentSchoolYear):

    score_boards = (db.session.query(ScoreBoard.id, Student.name, Student.dob)
                    .join(Class)
                    .join(Subject)
                    .join(Semester)
                    .join(Student)
                    .filter(Class.name == className, Subject.name == subjectName,
                            Semester.name == f'{semester}_{currentSchoolYear}').all())
    return score_boards

def getClass(Class_ID):
    cl = db.session.query(Class).filter(Class.id==Class_ID).first()
    return cl



def getClassesByTeacher(teacherId, kw=None):
    list_class = (db.session.query(TeacherClass, Class.name, Class.size,Class.id)
                  .join(Class)
                  .filter(TeacherClass.teacher_id == teacherId)
                  )
    if kw:
        list_class = list_class.filter(Class.name.contains(kw))
    return list_class.all()


def getSubjectByUser(teacherId):
    return db.session.query(Subject).join(User).filter(User.id == teacherId).first()


def getClassByGradeAndSchoolYear(grade, schoolYear):
    classes = (db.session.query(Class)
               .join(Grade)
               .join(ScoreBoard)
               .join(Semester)
               .filter(Grade.name == grade, Semester.name.contains(schoolYear))
               .all())
    print(classes)
    return classes


def getClassesByTeacherAndCurrentSchoolYear(teacherId, currentSchoolYear):
    return (db.session.query(TeacherClass, Class.name, Class.size)
            .join(Class)
            .join(ScoreBoard)
            .join(Semester)
            .filter(TeacherClass.teacher_id == teacherId,
                    Semester.name.contains(currentSchoolYear))
            .all())


def getSubjectByUser(teacherId):
    return db.session.query(Subject).join(User).filter(User.id == teacherId).first()


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


def get_grade():
    return db.session.query(Grade).all()


class StudentStats:
    def __init__(self, grade_name, student_name, class_name, avg_score, grade_type):
        self.grade_name = grade_name
        self.student_name = student_name
        self.class_name = class_name
        self.avg_score = avg_score
        self.grade_type = grade_type


def type_sort_avg_score(avg_score):
    if avg_score >= 8:
        return "Giỏi"
    elif avg_score >= 6.5:
        return "Khá"
    elif avg_score >= 5:
        return "Trung bình"
    else:
        return "Yếu"


def types_stats_by_grade(grade="10"):
    # viet phan loai tung hoc sinh trong khoi, xuat khoi, loai hs, so luong)

    result = []
    if grade:
        query = db.session.query(Grade.name, Student.name, Class.name, func.round(func.avg(Score.value), 2)) \
            .join(Class) \
            .join(ScoreBoard) \
            .join(Student) \
            .join(Subject) \
            .join(Score) \
            .group_by(Student.name, Class.name) \
            .filter(Grade.name == grade) \
            .order_by(desc(func.round(func.avg(Score.value), 2)))

        result = [StudentStats(grade_name, student_name, class_name, avg_score, type_sort_avg_score(avg_score))
                  for grade_name, student_name, class_name, avg_score in query.all()]

    # print(result)

    return result


def scores_stats(score_min=0, score_max=10, semester="HK1_23-24", subject="Toán", classroom="10A7"):
    query = db.session.query(func.round(Score.value, 0), func.count(func.round(Score.value, 0))) \
        .join(ScoreBoard, ScoreBoard.id == Score.score_board_id) \
        .join(Semester, Semester.id == ScoreBoard.semester_id) \
        .join(Subject, Subject.id == ScoreBoard.subject_id) \
        .join(Class, Class.id == ScoreBoard.class_id) \
        .group_by(func.round(Score.value, 0)) \
        .order_by(asc(func.round(Score.value, 0)))

    if score_min:
        query = query.filter(Score.value >= score_min)
    if score_max:
        query = query.filter(Score.value <= score_max)
    if semester:
        query = query.filter(Semester.name.contains(semester))
    if subject:
        query = query.filter(Subject.name.contains(subject))
    if classroom:
        query = query.filter(Class.name.contains(classroom))

    print(query.all())

    return query.all()


def passed_stats():
    pass


def insert_score(dataScores):
    print(dataScores)
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
