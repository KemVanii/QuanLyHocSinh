from app.models import *
from sqlalchemy import func, desc, asc, text, or_, and_
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
                'endpoint': 'student',
                'icon': 'fa-solid fa-book'
            },
            {
                'name': 'Lập danh sách',
                'endpoint': 'lapdanhsach',
                'icon': 'fa-solid fa-bars'
            },
            {
                'name': 'Điều chỉnh danh sách',
                'endpoint': 'dieuchinhdanhsach',
                'icon': 'fa-solid fa-list'
            },
        ]
    elif user_role == UserRoleEnum.Teacher:
        return [
            {
                'name': 'Home',
                'endpoint': '',
                'icon': 'fa-solid fa-home'
            },
            {
                'name': 'Nhập Điểm',
                'endpoint': 'nhapdiem',
                'icon': 'fa-solid fa-star'
            },
            {
                'name': 'Chỉnh sửa Điểm',
                'endpoint': 'chinhsuadiem',
                'icon': 'fa-solid fa-scroll'
            },
            {
                'name': 'Xem Điểm',
                'endpoint': 'xemdiem',
                'icon': 'fa-solid fa-magnifying-glass'
            }
        ]
    elif user_role == UserRoleEnum.Admin:
        return [
            {
                'name': 'Quy định',
                'endpoint': 'quydinh',
                'icon': 'fa-solid fa-scroll'
            },
            {
                'name': 'Thống kê',
                'endpoint': 'thongke',
                'icon': 'fa-solid fa-chart-simple'
            },
            {
                'name': 'Tài khoản',
                'endpoint': 'user',
                'icon': 'fa-solid fa-user'
            },
            {
                'name': 'Môn học',
                'endpoint': 'subject',
                'icon': 'fa-solid fa-book-bookmark'
            },

        ]
    return []


def getStudentsNotHasClass(limit=None):
    query = db.session.query(Student).filter(Student.score_boards == None)
    if limit:
        query = query.limit(limit)
    return query.all()


def getStudentsRemoveClass(grade, schoolYear):
    return (db.session.query(Student)
            .join(ScoreBoard)
            .join(Class)
            .join(Grade)
            .join(Semester)
            .filter(Grade.name == grade,
                    Semester.name.contains(schoolYear),
                    ScoreBoard.status == False)
            .all())


def getStudentsHasClass(grade, schoolYear):
    return (db.session.query(ScoreBoard, Student, Class)
            .join(Class)
            .join(Grade)
            .join(Semester)
            .join(Student)
            .filter(Grade.name == grade,
                    Semester.name == f"HK1_{schoolYear}",
                    ScoreBoard.status == True)
            .all())


def getScoreBoard(className, subjectName, semester, currentSchoolYear):
    score_boards = (db.session.query(ScoreBoard, ScoreBoard.id, Student.name, Student.dob)
                    .join(Class)
                    .join(Subject)
                    .join(Semester)
                    .join(Student)
                    .filter(Class.name == className, Subject.name == subjectName,
                            ScoreBoard.status == True,
                            Semester.name == f'{semester}_{currentSchoolYear}').all())
    return score_boards


def getScoreBoardByClass(classId, subjectId, semester):
    return (db.session.query(ScoreBoard, ScoreBoard.id, Student.name, Student.dob, Student.email)
            .join(Subject)
            .join(Semester)
            .join(Student)
            .filter(ScoreBoard.class_id == classId,
                    ScoreBoard.subject_id == subjectId,
                    ScoreBoard.status == True,
                    Semester.name.contains(semester)).all())


def getStudentsAlreadyStudyGradeInSchoolYear(grade, schoolYear):
    return (db.session.query(Student)
            .join(ScoreBoard)
            .join(Class)
            .join(Grade)
            .join(Semester)
            .filter(Grade.name == grade,
                    Semester.name.contains(schoolYear))
            .all())


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
    return (db.session.query(Class)
            .filter(Class.id == Class_ID).first())


def getSemesterByClassId(Class_ID):
    return (db.session.query(Semester)
            .join(ScoreBoard)
            .join(Class)
            .filter(Class.id == Class_ID)
            .all())


def getSemestersBySchoolYear(schoolYear):
    return (db.session.query(Semester)
            .filter(Semester.name.contains(schoolYear))
            .all())


def getClassesByTeacher(teacherId, schoolYear, kw=None):
    list_class = (db.session.query(TeacherClass, Class.name, Class.size, Class.id)
                  .join(Class)
                  .join(ScoreBoard)
                  .join(Semester)
                  .filter(TeacherClass.teacher_id == teacherId,
                          Semester.name.contains(schoolYear)))
    if kw:
        list_class = list_class.filter(Class.name.contains(kw))
    return list_class.all()


def getSubjectByUser(teacherId):
    return db.session.query(Subject).join(User).filter(User.id == teacherId).first()


def getClassByGradeAndSchoolYear(grade, schoolYear):
    classes = (db.session.query(Class, Semester.name)
               .join(Grade)
               .join(ScoreBoard)
               .join(Semester)
               .filter(Grade.name == grade, Semester.name == f"HK1_{schoolYear}")
               .all())

    return classes


def get_class_by_school_year(school_year):
    grade = db.session.query(Grade).join(Class).filter(Class.grade_id == Grade.id).first()
    classes = getClassByGradeAndSchoolYear(grade=grade.name, schoolYear=school_year)

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
    return (db.session.query(Class, Grade.name)
            .join(Grade)
            .filter(Class.id == classId)
            .first())


def getGradeByClassId(classId):
    return (db.session.query(Grade)
            .join(Class)
            .filter(Class.id == classId)
            .first())


def getStudentListByClassId(classId):
    return (db.session.query(Student)
            .join(ScoreBoard)
            .filter(ScoreBoard.class_id == classId,
                    ScoreBoard.status == True)
            .all())


def deleteStudentFromClass(studentId, classId, schoolYear):
    score_boards = (db.session.query(ScoreBoard)
                    .join(Semester)
                    .filter(ScoreBoard.class_id == classId,
                            ScoreBoard.student_id == studentId,
                            Semester.name.contains(schoolYear))
                    .all())
    for score_board in score_boards:
        score_board.status = False
    cla = db.session.query(Class).filter(Class.id == classId).first()
    cla.size = cla.size - 1
    db.session.commit()


def insertStudentToClass(studentId, classId, schoolYear):
    score_boards = (db.session.query(ScoreBoard)
                    .join(Semester)
                    .filter(ScoreBoard.student_id == studentId,
                            Semester.name.contains(schoolYear))
                    .all())
    if len(score_boards) == 0:  # case new Student
        subjects = (db.session.query(Subject)
                    .join(User)
                    .join(TeacherClass)
                    .filter(TeacherClass.class_id == classId)).all()
        semesters = db.session.query(Semester).filter(Semester.name.contains(schoolYear)).all()
        for subject in subjects:
            for semester in semesters:
                sb = ScoreBoard(student_id=studentId, subject_id=subject.id, class_id=classId,
                                semester_id=semester.id)
                db.session.add(sb)
    else:  # case student have been deleted
        for score_board in score_boards:
            score_board.class_id = classId
            score_board.status = True
    cla = db.session.query(Class).filter(Class.id == classId).first()
    cla.size = cla.size + 1
    db.session.commit()


def getSubjectByUser(teacherId):
    return db.session.query(Subject).join(User).filter(User.id == teacherId).first()


def getAllSubject():
    return db.session.query(Subject).all()


def createNewClassGrade(className, students, size, grade, currentSchoolYear):
    # Create new Class
    grade_id = db.session.query(Grade).filter(Grade.name == grade).first().id
    newClass = Class(name=className, size=size, grade_id=grade_id)
    db.session.add(newClass)
    db.session.commit()
    db.session.refresh(newClass)

    # Create new Score_Boards
    subjects = getAllSubject()
    semesters = db.session.query(Semester).filter(Semester.name.contains(currentSchoolYear)).all()
    for student in students:
        print(student)
        score_boards = (db.session.query(ScoreBoard)
                        .join(Semester)
                        .filter(ScoreBoard.student_id == student.id,
                                Semester.name.contains(currentSchoolYear))
                        .all())

        if len(score_boards) == 0:
            for semester in semesters:
                for subject in subjects:
                    newScoreBoard = ScoreBoard(student_id=student.id, subject_id=subject.id,
                                               class_id=newClass.id, semester_id=semester.id,
                                               status=True)
                    db.session.add(newScoreBoard)
        else:
            for score_board in score_boards:
                score_board.class_id = newClass.id
                score_board.status = True

    # Create new TeacherClass
    teachers = db.session.query(User).filter(User.user_role == UserRoleEnum.Teacher).all()
    for subject in subjects:
        filterTeacherBySubject = [teacher for teacher in teachers if teacher.subject_id == subject.id]
        newTeacherClass = TeacherClass(teacher_id=random.choice(filterTeacherBySubject).id, class_id=newClass.id)
        db.session.add(newTeacherClass)
    db.session.commit()


def get_semester_by_school_year(school_year):
    if school_year is None:
        school_year = app.config['school_year']

    return db.session.query(Semester).filter(Semester.name.like(f'%{school_year}%')).all()


def get_subject():
    return db.session.query(Subject).all()


def get_grade():
    return db.session.query(Grade).all()


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

    return query.all()


def get_scoreboards_by_student_semester(student, semester):
    query = db.session.query(ScoreBoard).join(Student).join(Semester).filter(Student.id == student,
                                                                             Semester.name == semester).all()

    return query


def get_class_by_name(name):
    return db.session.query(Class).filter(Class.name == name).first()


def grade_type_stats_by_class(classroom_name):
    classroom = get_class_by_name(classroom_name)
    students_in_class = getStudentListByClassId(classroom.id)
    grade = getGradeByClassId(classroom.id)
    semester = "HK1_23-24"
    classroom = getClass(classroom.id)
    result = {}
    if students_in_class:
        for s in students_in_class:
            score_boards = get_scoreboards_by_student_semester(s.id, semester)
            total_coefficient = 0
            avg_score = 0
            if score_boards is not None:
                for score_board in score_boards:
                    avg_score = avg_score + calSemesterAverage(score_board.scores)
                    total_coefficient = total_coefficient + 1
                result_avg_score = avg_score / total_coefficient
                grade_type = type_sort_avg_score(result_avg_score)
                result[s.id] = {
                    "semester": semester,
                    "grade": grade.name,
                    "class": classroom.name,
                    "student_id": s.id,
                    "student_name": s.name,
                    "avg_score": round(result_avg_score, 2),
                    "grade_type": grade_type
                }

    return result


def get_students_in_grade(grade_name):
    return db.session.query(Student).join(ScoreBoard).join(Class).join(Grade).filter(Grade.name == grade_name)


def get_classes_by_student_id(student_id):
    return db.session.query(Class).join(ScoreBoard).join(Student).filter(Student.id == student_id).first()


def grade_type_stats_by_grade(grade_name):
    students_in_grade = get_students_in_grade(grade_name)
    grade = db.session.query(Grade).filter(Grade.name == grade_name).first()
    semester = "HK1_23-24"
    result = {}
    if students_in_grade:
        for s in students_in_grade:
            score_boards = get_scoreboards_by_student_semester(s.id, semester)
            classroom = get_classes_by_student_id(s.id)
            total_coefficient = 0
            avg_score = 0
            if score_boards is not None:
                for score_board in score_boards:
                    avg_score = avg_score + calSemesterAverage(score_board.scores)
                    total_coefficient = total_coefficient + 1
                result_avg_score = avg_score / total_coefficient
                grade_type = type_sort_avg_score(result_avg_score)
                result[s.id] = {
                    "semester": semester,
                    "grade": grade.name,
                    "class": classroom.name,
                    "student_id": s.id,
                    "student_name": s.name,
                    "avg_score": round(result_avg_score, 2),
                    "grade_type": grade_type
                }

    return result


def grade_type_stats(classroom_name, grade_name):
    result = {}
    if classroom_name:
        result = grade_type_stats_by_class(classroom_name)
    if grade_name:
        result = grade_type_stats_by_grade(grade_name)

    print(result)
    return result


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


def update_score(dataScores):
    for dataScore in dataScores:
        Score.query.filter(Score.score_board_id == dataScore['score_board_id']).delete()
        for i in range(len(dataScore['15p'])):
            s = Score(value=dataScore['15p'][i], type='15p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        for i in range(len(dataScore['45p'])):
            s = Score(value=dataScore['45p'][i], type='45p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        s = Score(value=dataScore['ck'], type='ck', score_board_id=dataScore['score_board_id'])
        db.session.add(s)
    db.session.commit()


def getSemesterTeacher(TeaderId):
    return (db.session.query(Semester)
            .join(ScoreBoard)
            .join(Class)
            .join(TeacherClass)
            .filter(TeacherClass.teacher_id == TeaderId,
                    Semester.name.contains('HK1'))
            .all())

# def getScore(ScoreBoard_id):
#     list_Score=db.session.query(ScoreBoard).join(Score).filter(Score.id==ScoreBoard_id).all()
#     return list_Score
# def getScoreBoardByClassID(ClassID):
#     ScoreBoardID=db.session.query(ScoreBoard).join(Class).filter(Class.id==ClassID).first()


# read json and write json
