from app.models import *
from sqlalchemy import func, desc, asc, text, or_, and_
from collections import defaultdict
from app import db
from app.util import *
from app.models import ScoreBoard, Score
from app.util import filter_student, get_previous_school_year
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
    query = (db.session.query(Student)
             .filter(Student.score_boards == None,
                     Student.isTransferSchool == False))
    if limit:
        query = query.limit(limit)
    return query.all()


def getStudentsTranferSchool():
    return db.session.query(Student).filter(Student.score_boards == None,
                                            Student.isTransferSchool == True).all()


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


def getStudentsHasClass(grade, schoolYear, exceptClassId):
    return (db.session.query(ScoreBoard.student_id, Student, Class)
            .distinct(ScoreBoard.student_id)
            .join(Class)
            .join(Grade)
            .join(Semester)
            .join(Student)
            .filter(Grade.name == grade,
                    Semester.name.contains(schoolYear),
                    ScoreBoard.status == True,
                    ScoreBoard.class_id != exceptClassId)
            .order_by(Class.name)
            .all())


def getScoreBoardByClass(classId, subjectId, semester):
    return (db.session.query(ScoreBoard, ScoreBoard.id, Student.name, Student.dob, Student.email)
            .join(Subject)
            .join(Semester)
            .join(Student)
            .filter(ScoreBoard.class_id == classId,
                    ScoreBoard.subject_id == subjectId,
                    ScoreBoard.status == True,
                    Semester.name.contains(semester)).all())


def getStudentsAlreadyStudyButNotInCurrSchoolYear(grade, prevSchoolYear, currSchoolYear):
    return (db.session.query(Student)
            .join(ScoreBoard)
            .join(Class)
            .join(Grade)
            .join(Semester)
            .filter(Grade.name == grade,
                    Semester.name.contains(prevSchoolYear),
                    ~Semester.name.contains(currSchoolYear))
            .all())


def getStudentsPassOrFailInGradeInPreSchoolYear(grade, currSchoolYear, result):
    # lấy niên học trước
    prevSchoolYear = get_previous_school_year(currSchoolYear)
    # lấy sách học sinh đã ở niên học trước của khối đó
    StudentsAlreadyStudyButNotInCurrSchoolYear = (
        getStudentsAlreadyStudyButNotInCurrSchoolYear(grade, prevSchoolYear, currSchoolYear))
    prevSemesters = getSemestersBySchoolYear(prevSchoolYear)
    return filter_student(StudentsAlreadyStudyButNotInCurrSchoolYear, prevSemesters,
                          result)


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


def getClassesByTeacherAndSchoolYear(teacherId, schoolYear, kw=None):
    list_class = (db.session.query(TeacherClass, Class.name, Class.size, Class.id)
                  .join(Class)
                  .join(ScoreBoard)
                  .join(Semester)
                  .filter(TeacherClass.teacher_id == teacherId,
                          Semester.name.contains(schoolYear))
                  .order_by(Class.name))
    if kw:
        list_class = list_class.filter(Class.name.contains(kw))
    return list_class.all()


def getClassByGradeAndSchoolYear(grade, schoolYear):
    classes = (db.session.query(Class, Semester.name)
               .join(Grade)
               .join(ScoreBoard)
               .join(Semester)
               .filter(Grade.name == grade, Semester.name == f"HK1_{schoolYear}")
               .order_by(Class.name)
               .all())

    return classes


def get_class_by_school_year(school_year):
    grade = db.session.query(Grade).join(Class).filter(Class.grade_id == Grade.id).first()
    classes = getClassByGradeAndSchoolYear(grade=grade.name, schoolYear=school_year)
    return classes


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
    if len(score_boards) == 0:  # Trường hợp học sinh mới
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
    else:  # Trường hợp học sinh bị xóa khỏi lớp hoặc đang chuyển lớp
        classIdOld = score_boards[0].class_id
        classOld = db.session.query(Class).filter(Class.id == classIdOld).first()
        classOld.size = classOld.size - 1
        for score_board in score_boards:
            score_board.class_id = classId
            score_board.status = True
    classNew = db.session.query(Class).filter(Class.id == classId).first()
    classNew.size = classNew.size + 1
    db.session.commit()


def getAllSubject():
    return db.session.query(Subject).filter(Subject.status == True).all()


def getSubjectByUser(teacherId):
    return db.session.query(Subject).join(User).filter(User.id == teacherId).first()


def getSubjectByClassAndYear(className, currentSchoolYear):
    subjects = (db.session.query(Subject)
                .join(ScoreBoard)
                .join(Class)
                .join(Semester)
                .filter(Class.name == className,
                        Semester.name.contains(currentSchoolYear))
                .all())
    return subjects


def getStudentsForCreateNewClass(grade, currSchoolYear, size):
    students = []
    studentsRemoveClass = getStudentsRemoveClass(grade, currSchoolYear)
    studentsFailThisGradeInPrevSchoolYear = (
        getStudentsPassOrFailInGradeInPreSchoolYear(grade, currSchoolYear,
                                                        False))
    if grade == 10:
        studentNotHasClass = getStudentsNotHasClass()
        students = (studentNotHasClass
                    + studentsRemoveClass
                    + studentsFailThisGradeInPrevSchoolYear)

    else:
        studentsPassPreGradeInPrevSchoolYear = (
            getStudentsPassOrFailInGradeInPreSchoolYear(grade - 1,
                                                            currSchoolYear,
                                                            True))
        students = (studentsPassPreGradeInPrevSchoolYear
                    + studentsRemoveClass
                    + studentsFailThisGradeInPrevSchoolYear)
    students = students[:int(size)]
    return students


def createNewClassGrade(className, students, grade, currentSchoolYear):
    subjectNotHasTeacher = db.session.query(Subject).filter(Subject.teachers == None).all()
    if subjectNotHasTeacher:
        return
    # Tạo lớp mới
    grade_id = db.session.query(Grade).filter(Grade.name == grade).first().id
    newClass = Class(name=className, size=len(students), grade_id=grade_id)
    db.session.add(newClass)
    db.session.commit()
    db.session.refresh(newClass)

    # Tạo danh sách bảng điểm cho lớp đó
    subjects = getAllSubject()
    semesters = db.session.query(Semester).filter(Semester.name.contains(currentSchoolYear)).all()
    for student in students:
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

    # Tạo danh sách giáo viên bộ môn cho lớp đó
    teachers = db.session.query(User).filter(User.user_role == UserRoleEnum.Teacher).all()
    for subject in subjects:
        filterTeacherBySubject = []
        for teacher in teachers:
            if teacher.subject_id == subject.id:
                filterTeacherBySubject.append(teacher)
        if len(filterTeacherBySubject) != 0:
            newTeacherClass = TeacherClass(teacher_id=random.choice(filterTeacherBySubject).id, class_id=newClass.id)
            db.session.add(newTeacherClass)

    db.session.commit()


def get_semester():
    return db.session.query(Semester).all()


def get_semester_by_school_year(school_year):
    if school_year is None:
        school_year = app.config['school_year']

    return db.session.query(Semester).filter(Semester.name.like(f'%{school_year}%')).all()


def get_subject():
    return db.session.query(Subject).all()


def get_grade():
    return db.session.query(Grade).all()


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


def get_class_by_name(name):
    return db.session.query(Class).filter(Class.name == name).first()


def get_students_by_class_semester(class_id, semester):
    return db.session.query(Student).join(ScoreBoard).join(Semester).filter(ScoreBoard.class_id == class_id,
                                                                            Semester.name == semester).all()


def get_scoreboards_by_student(student_id, semester):
    return db.session.query(ScoreBoard).join(Semester).filter(ScoreBoard.student_id == student_id,
                                                              Semester.name == semester).all()


def grade_type_stats_by_class(classroom_name, semester):
    classroom = get_class_by_name(classroom_name)
    students_in_class = get_students_by_class_semester(classroom.id, semester)
    total_coefficient = 0
    avg_score = 0
    result = {}
    if students_in_class:
        for s in students_in_class:
            score_boards = get_scoreboards_by_student(s.id, semester)
            if score_boards:
                for score_board in score_boards:
                    if len(score_board.scores) == 0:
                        return {}
                    avg_score = avg_score + calSemesterAverage(score_board.scores)
                    total_coefficient = total_coefficient + 1
                result_avg_score = avg_score / total_coefficient
                grade_type = type_sort_avg_score(result_avg_score)
                result[s.id] = {
                    "semester": semester,
                    "grade": classroom.grade_id,
                    "class": classroom.name,
                    "student_id": s.id,
                    "student_name": s.name,
                    "avg_score": round(result_avg_score, 2),
                    "grade_type": grade_type
                }
                total_coefficient = 0
                avg_score = 0

    return result


def get_grade_by_name(grade_name):
    return db.session.query(Grade).filter(Grade.name == grade_name).first()


def get_students_by_grade_semester(grade_id, semester):
    return db.session.query(Student).join(ScoreBoard).join(Class).join(Semester).filter(Class.grade_id == grade_id,
                                                                                        Semester.name == semester).all()


def get_class_by_student(student_id):
    return db.session.query(Class).join(ScoreBoard).filter(ScoreBoard.student_id == student_id).first()


def grade_type_stats_by_grade(grade_name, semester):
    grade = get_grade_by_name(grade_name)
    students_in_grade = get_students_by_grade_semester(grade.id, semester)
    result = {}
    total_coefficient = 0
    avg_score = 0
    if students_in_grade:
        for s in students_in_grade:
            score_boards = get_scoreboards_by_student(s.id, semester)
            if score_boards:
                for score_board in score_boards:
                    if len(score_board.scores) == 0:
                        return {}
                    avg_score = avg_score + calSemesterAverage(score_board.scores)
                    total_coefficient = total_coefficient + 1
                result_avg_score = avg_score / total_coefficient
                grade_type = type_sort_avg_score(result_avg_score)
                classroom = getClass(score_board.class_id)
                result[s.id] = {
                    "semester": semester,
                    "grade": grade.name,
                    "class": classroom.name,
                    "student_id": s.id,
                    "student_name": s.name,
                    "avg_score": round(result_avg_score, 2),
                    "grade_type": grade_type
                }
                total_coefficient = 0
                avg_score = 0

    return result


def grade_type_stats(classroom_name, grade_name, semester_name):
    result = {}
    if classroom_name and semester_name:
        result = grade_type_stats_by_class(classroom_name, semester_name)
    if grade_name and semester_name:
        result = grade_type_stats_by_grade(grade_name, semester_name)

    return result


def insert_score(dataScores):
    for dataScore in dataScores:
        for value in dataScore['15p']:
            s = Score(value=value, type='15p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        for value in dataScore['45p']:
            s = Score(value=value, type='45p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        s = Score(value=dataScore['ck'], type='ck', score_board_id=dataScore['score_board_id'])
        db.session.add(s)
        db.session.commit()


def update_score(dataScores):
    for dataScore in dataScores:
        Score.query.filter(Score.score_board_id == dataScore['score_board_id']).delete()
        for value in dataScore['15p']:
            s = Score(value=value, type='15p', score_board_id=dataScore['score_board_id'])
            db.session.add(s)
        for value in dataScore['45p']:
            s = Score(value=value, type='45p', score_board_id=dataScore['score_board_id'])
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

# read json and write json
