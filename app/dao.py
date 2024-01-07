from app.models import *
from sqlalchemy import func, desc, asc, text
from collections import defaultdict
from app import db
from app.util import *
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
    score_boards = (db.session.query(ScoreBoard, ScoreBoard.id, Student.name, Student.dob)
                    .join(Class)
                    .join(Subject)
                    .join(Semester)
                    .join(Student)
                    .filter(Class.name == className, Subject.name == subjectName,
                            Semester.name == f'{semester}_{currentSchoolYear}').all())
    return score_boards


def getScoreBoardByClassStudentYear(className, studentId, currentSchoolYear):
    score_boards = (db.session.query(ScoreBoard)
                    .join(Class)
                    .join(Student)
                    .join(Semester)
                    .filter(Class.name == className, Student.id == studentId,
                            Semester.name.contains(currentSchoolYear)).all())
    return score_boards


def getSubjectByClassAndYear(className, currentSchoolYear):
    subjects = (db.session.query(Subject)
                .join(ScoreBoard)
                .join(Class)
                .join(Semester)
                .filter(Class.name == className,
                        Semester.name.contains(currentSchoolYear))
                .all())
    return subjects


def getClass(Class_ID):
    cl = db.session.query(Class).filter(Class.id == Class_ID).first()
    return cl


def getClassesByTeacher(teacherId, kw=None):
    list_class = (db.session.query(TeacherClass, Class.name, Class.size, Class.id)
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
    return classes


def getClassesByTeacherAndCurrentSchoolYear(teacherId, currentSchoolYear="HK1_23-24"):
    return (db.session.query(TeacherClass, Class.name, Class.size)
            .join(Class)
            .join(ScoreBoard)
            .join(Semester)
            .filter(TeacherClass.teacher_id == teacherId,
                    Semester.name.contains(currentSchoolYear))
            .all())


def getClassById(classId):
    return db.session.query(Class).filter(Class.id == classId).first()


def getStudentListByClassId(classId):
    return (db.session.query(Student)
            .join(ScoreBoard)
            .filter(ScoreBoard.class_id == classId,
                    ScoreBoard.status == True)
            .all())


def deleteStudentInClass(studentId, classId, schoolYear):
    print(studentId, classId, schoolYear)
    score_boards = (db.session.query(ScoreBoard)
                    .join(Semester)
                    .filter(ScoreBoard.class_id == classId,
                            ScoreBoard.student_id == studentId,
                            Semester.name.contains(schoolYear))
                    .all())
    for score_board in score_boards:
        score_board.status = False
    db.session.commit()


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


def type_sort_avg_score(avg_score):
    if avg_score >= 8:
        return "Giỏi"
    elif avg_score >= 6.5:
        return "Khá"
    elif avg_score >= 5:
        return "Trung bình"
    else:
        return "Yếu"


def types_stats(classroom, grade):
    # viet phan loai tung hoc sinh trong khoi, xuat khoi, loai hs, so luong)
    query = db.session.query(Grade.name, Student.name, Class.name, func.round(func.avg(Score.value), 2)) \
        .join(Class) \
        .join(ScoreBoard) \
        .join(Student) \
        .join(Subject) \
        .join(Score) \
        .group_by(Grade.name, Student.name, Class.name) \
        .order_by(asc(Grade.name), desc(func.round(func.avg(Score.value), 2)))

    # query = db.session.query(Grade.name, Student.name, Class.name, func.round(calSemesterAverage(Score.value), 2)) \
    #     .join(Class) \
    #     .join(ScoreBoard) \
    #     .join(Student) \
    #     .join(Subject) \
    #     .join(Score) \
    #     .group_by(Grade.name, Student.name, Class.name) \
    #     .order_by(asc(Grade.name), desc(func.round(calSemesterAverage(Score.value), 2)))

    print(query.all())

    if classroom:
        query = query.filter(Class.name == classroom)
    if grade:
        query = query.filter(Grade.name == grade)

    result = query.all()

    result_info = defaultdict(lambda: defaultdict(int))

    for grade_name, _, _, avg_score in result:
        grade_type = type_sort_avg_score(avg_score)
        result_info[grade_name][grade_type] += 1

    result_summary = [
        (grade_name, grade_type, count)
        for grade_name, grade_data in result_info.items()
        for grade_type, count in grade_data.items()
    ]

    return result_summary


def types_stats_by_grade():
    pass


def scores_stats(score_min, score_max, semester, subject, classroom):
    query = db.session.query(func.round(Score.value, 0), func.count(func.round(Score.value, 0))) \
        .join(ScoreBoard) \
        .join(Semester) \
        .join(Subject) \
        .join(Class) \
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
    for dataScore in dataScores:
        for i in range(len(dataScore['15p'])):
            s = Score(value=dataScore['15p'][i], type='15p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        for i in range(len(dataScore['45p'])):
            s = Score(value=dataScore['45p'][i], type='45p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        s = Score(value=dataScore['ck'], type='ck', score_board_id=dataScore['score_board_id'])
        db.session.add(s)
        db.session.commit()

# def getScore(ScoreBoard_id):
#     list_Score=db.session.query(ScoreBoard).join(Score).filter(Score.id==ScoreBoard_id).all()
#     return list_Score
# def getScoreBoardByClassID(ClassID):
#     ScoreBoardID=db.session.query(ScoreBoard).join(Class).filter(Class.id==ClassID).first()


# read json and write json
