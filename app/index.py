import hashlib
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user
from app import app, login
from app.models import *
from app.auth import restrict_to_roles
from app.util import isPass, calSemesterAverage, loadPolicies, filter_student, get_previous_school_year
from app.mailService import send_email
import dao


@login.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    funcs = dao.load_function(current_user.user_role)
    classes = []
    if current_user.user_role == UserRoleEnum.Teacher:
        classes = dao.getClassesByTeacherAndCurrentSchoolYear(current_user.id, app.config["school_year"])
    return render_template('index.html', funcs=funcs, classes=classes, school_year=app.config["school_year"],
                           user_role=UserRoleEnum.Employee)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        if (user and user.password == str(hashlib.md5(request.form.get("pswd").encode('utf-8')).hexdigest())
                and user.status is True):
            login_user(user)
            loadPolicies(app)
            next_url = request.args.get("next_url")
            if next_url is not None:
                return redirect(url_for(next_url))
            return redirect(url_for("index"))

    next_url = request.args.get('next_url') or 'index'
    return render_template("login.html", next_url=next_url)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/tiepnhanhocsinh')
@restrict_to_roles([UserRoleEnum.Employee])
def tiepNhanHocSinh():
    return redirect('/student')


@app.route('/lapdanhsach', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Employee], next_url='lapdanhsach')
def lapdanhsach():
    currSchoolYear = app.config['school_year']
    if request.method == "POST":
        size = int(request.form.get("inputSize"))
        grade = int(request.form.get("inputGrade"))
        print(grade)
        newNameClass = f'{grade}/{len(dao.getClassByGradeAndSchoolYear(grade, currSchoolYear)) + 1}'
        prevSchoolYear = get_previous_school_year(currSchoolYear)
        prevSemesters = dao.getSemestersBySchoolYear(prevSchoolYear)  # get semester of previous schoolYear
        currSemester = dao.getSemestersBySchoolYear(currSchoolYear)
        studentsRemoveClass = dao.getStudentsRemoveClass(grade, currSchoolYear)
        StudentsAlreadyStudy = dao.getStudentsAlreadyStudyGradeInSchoolYear(grade, prevSchoolYear)
        studentsFailThisGradeInPrevSchoolYear = filter_student(StudentsAlreadyStudy,
                                                               prevSemesters,
                                                               currSemester,
                                                               False)
        if grade == 10:
            studentNotHasClass = dao.getStudentsNotHasClass()
            students = (studentNotHasClass
                        + studentsRemoveClass
                        + studentsFailThisGradeInPrevSchoolYear)

        else:
            StudentsAlreadyStudy = dao.getStudentsAlreadyStudyGradeInSchoolYear(grade - 1, prevSchoolYear)
            studentsPassPreGradeInPrevSchoolYear = filter_student(StudentsAlreadyStudy,
                                                                  prevSemesters,
                                                                  currSemester,
                                                                  True)
            students = (studentsPassPreGradeInPrevSchoolYear
                        + studentsRemoveClass
                        + studentsFailThisGradeInPrevSchoolYear)
        students = students[:int(size)]
        dao.createNewClassGrade(newNameClass, students, size, grade, currSchoolYear)
        return redirect(url_for('lapdanhsach'))

    funcs = dao.load_function(current_user.user_role)
    maxSize = app.config['max_class_size']
    size = request.args.get("inputSize") or ''
    grade = int(request.args.get("inputGrade") or '10')
    students = []
    newNameClass = ''
    if size:
        newNameClass = f'{grade}/{len(dao.getClassByGradeAndSchoolYear(grade, currSchoolYear)) + 1}'
        prevSchoolYear = get_previous_school_year(currSchoolYear)
        prevSemesters = dao.getSemestersBySchoolYear(prevSchoolYear)  # get semester of previous schoolYear
        currSemester = dao.getSemestersBySchoolYear(currSchoolYear)
        studentsRemoveClass = dao.getStudentsRemoveClass(grade, currSchoolYear)
        StudentsAlreadyStudy = dao.getStudentsAlreadyStudyGradeInSchoolYear(grade, prevSchoolYear)
        studentsFailThisGradeInPrevSchoolYear = filter_student(StudentsAlreadyStudy,
                                                               prevSemesters,
                                                               currSemester,
                                                               False)
        if grade == 10:
            studentNotHasClass = dao.getStudentsNotHasClass()
            students = (studentNotHasClass
                        + studentsRemoveClass
                        + studentsFailThisGradeInPrevSchoolYear)

        else:
            StudentsAlreadyStudy = dao.getStudentsAlreadyStudyGradeInSchoolYear(grade - 1, prevSchoolYear)
            studentsPassPreGradeInPrevSchoolYear = filter_student(StudentsAlreadyStudy,
                                                                  prevSemesters,
                                                                  currSemester,
                                                                  True)
            students = (studentsPassPreGradeInPrevSchoolYear
                        + studentsRemoveClass
                        + studentsFailThisGradeInPrevSchoolYear)
        students = students[:int(size)]

    return render_template("lapDanhSach.html",
                           funcs=funcs, students=students,
                           size=size, grade=grade, maxSize=maxSize,
                           currentSchoolYear=currSchoolYear,
                           newNameClass=newNameClass)


@app.route('/dieuchinhdanhsach')
@restrict_to_roles([UserRoleEnum.Employee], next_url='dieuchinhdanhsach')
def dieuchinhdanhsach():
    funcs = dao.load_function(current_user.user_role)
    currentSchoolYear = app.config['school_year']
    grades = dao.get_grade()
    inputGrade = request.args.get('inputGrade') or 10
    classes = dao.getClassByGradeAndSchoolYear(inputGrade, currentSchoolYear)
    return render_template("dieuChinhDanhSach.html",
                           funcs=funcs, grades=grades,
                           inputGrade=inputGrade, classes=classes)


@app.route('/dieuchinhdanhsach/<int:idLop>', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Employee], next_url='dieuchinhdanhsach')
def dieuchinhdanhsachlop(idLop):
    currSchoolYear = app.config['school_year']
    if request.method == 'POST':
        action = request.form.get('action')
        studentId = request.form.get('student_id')
        if action == 'delete':
            dao.deleteStudentFromClass(studentId, idLop, currSchoolYear)
        elif action == 'add':
            dao.insertStudentToClass(studentId, idLop, currSchoolYear)
        return redirect(url_for('dieuchinhdanhsachlop', idLop=idLop))

    funcs = dao.load_function(current_user.user_role)
    grade = int(dao.getGradeByClassId(idLop).name)
    cla = dao.getClass(idLop)
    studentsInClass = dao.getStudentListByClassId(idLop)
    prevSchoolYear = get_previous_school_year(currSchoolYear)
    studentsForChangeClass = dao.getStudentsHasClass(grade, currSchoolYear)
    prevSemesters = dao.getSemestersBySchoolYear(prevSchoolYear)
    currSemester = dao.getSemestersBySchoolYear(currSchoolYear)
    studentsRemoveClass = dao.getStudentsRemoveClass(grade, currSchoolYear)
    StudentsAlreadyStudy = dao.getStudentsAlreadyStudyGradeInSchoolYear(grade, prevSchoolYear)
    studentsFailThisGradeInPrevSchoolYear = filter_student(StudentsAlreadyStudy,
                                                           prevSemesters,
                                                           currSemester,
                                                           False)
    if grade == 10:
        studentNotHasClass = dao.getStudentsNotHasClass()
        students = (studentNotHasClass
                    + studentsRemoveClass
                    + studentsFailThisGradeInPrevSchoolYear)

    else:
        StudentsAlreadyStudy = dao.getStudentsAlreadyStudyGradeInSchoolYear(grade - 1, prevSchoolYear)
        studentsPassPreGradeInPrevSchoolYear = filter_student(StudentsAlreadyStudy,
                                                              prevSemesters,
                                                              currSemester,
                                                              True)
        students = (studentsPassPreGradeInPrevSchoolYear
                    + studentsRemoveClass
                    + studentsFailThisGradeInPrevSchoolYear)
    return render_template("dieuChinhDanhSachlop.html",
                           funcs=funcs, studentsInClass=studentsInClass,
                           studentsNotInClass=students,
                           studentsForChangeClass=studentsForChangeClass,
                           cla=cla, idLop=idLop)


@app.route('/quydinh')
@restrict_to_roles([UserRoleEnum.Admin], next_url='quydinh')
def quydinh():
    funcs = dao.load_function(current_user.user_role)
    return render_template("quyDinh.html", funcs=funcs)


@app.route('/thongke', methods=["GET"])
@restrict_to_roles([UserRoleEnum.Admin], next_url='thongke')
def thongke():
    score_min = request.args.get('filterScoreMin')
    score_max = request.args.get('filterScoreMax')
    semester = request.args.get('semester')
    subject = request.args.get('subject')
    classroom = request.args.get('classroom')
    classroom_pie = request.args.get('classroomPie')
    grade_pie = request.args.get('gradePie')

    funcs = []

    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("thongKe.html", funcs=funcs,
                           score_stats=dao.scores_stats(score_min=score_min, score_max=score_max,
                                                        semester=semester,
                                                        subject=subject,
                                                        classroom=classroom),
                           grade_type_stats=dao.grade_type_stats(classroom_name=classroom_pie, grade_name=grade_pie),
                           semesters=dao.get_semester_by_school_year(school_year=semester),
                           subjects=dao.get_subject(),
                           classrooms=dao.get_class_by_school_year(school_year=app.config['school_year']),
                           grades=dao.get_grade())


@app.route('/nhapdiem', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Teacher], next_url='nhapdiem')
def nhapdiem():
    currentSchoolYear = app.config['school_year']
    if request.method == 'POST':
        # get all scores
        inputTenLop = request.form.get('inputTenLop')
        inputTenMon = request.form.get('inputTenMon')
        inputHocki = request.form.get('inputHocki')
        score_boards = dao.getScoreBoard(inputTenLop, inputTenMon, inputHocki, currentSchoolYear)
        score_boards_filter = []
        for score_board in score_boards:
            if len(score_board[0].scores) == 0:
                score_boards_filter.append(score_board)
        score_boards = score_boards_filter
        dataScores = []
        for score_board in score_boards:
            dataScore = {
                'score_board_id': score_board.id,
                '15p': request.form.getlist(f'15p{score_board.id}[]'),
                '45p': request.form.getlist(f'45p{score_board.id}[]'),
                'ck': request.form.get(f'ck{score_board.id}')
            }
            dataScores.append(dataScore)
        dao.insert_score(dataScores)
        return redirect(url_for('nhapdiem'))

    funcs = dao.load_function(current_user.user_role)
    inputTenLop = request.args.get('inputTenLop') or ''
    inputTenMon = dao.getSubjectByUser(current_user.id).name
    inputCot15p = int(request.args.get('inputCot15p') or '1')
    inputCot45p = int(request.args.get('inputCot45p') or '1')
    inputHocki = request.args.get('inputHocki')
    classes = dao.getClassesByTeacherAndCurrentSchoolYear(current_user.id, currentSchoolYear)
    score_boards = []

    if inputTenLop and inputHocki and inputCot15p and inputCot45p:
        score_boards = dao.getScoreBoard(inputTenLop, inputTenMon, inputHocki, currentSchoolYear)
        score_boards_filter = []
        for score_board in score_boards:
            if len(score_board[0].scores) == 0:
                score_boards_filter.append(score_board)
        score_boards = score_boards_filter

    return render_template("diem.html",
                           funcs=funcs, inputTenLop=inputTenLop, classes=classes,
                           inputCot15p=inputCot15p, inputCot45p=inputCot45p,
                           score_boards=score_boards, inputHocki=inputHocki,
                           inputTenMon=inputTenMon, currentSchoolYear=currentSchoolYear)


@app.route('/api/policy', methods=['post'])
def modify_policy():
    data = request.json

    policies = {
        "max_class_size": data.get('max_class_size'),
        "age_min": data.get('age_min'),
        "age_max": data.get('age_max'),
        "school_year": data.get("school_year")
    }

    session['policies'] = policies

    with open("static/policies.json", "w") as outfile:
        json.dump(policies, outfile)

    return jsonify(policies)


@app.route('/api/sendMail', methods=['post'])
def sendScoreViaEmail():
    idLop = request.form.get('idLop')
    hk = request.form.get('hk')
    score_boards = dao.getScoreBoardByClass(idLop, current_user.subject_id, f"HK{hk}")
    dataScores = []
    if score_boards and score_boards[0][0].scores:
        for score_board in score_boards:
            dataScore = {
                'student_name': score_board.name,
                'email': score_board.email,
                '15p': [score.value for score in score_board[0].scores if score.type == '15p'],
                '45p': [score.value for score in score_board[0].scores if score.type == '45p'],
                'ck': [score.value for score in score_board[0].scores if score.type == 'ck'][0],
                'dtb': round(calSemesterAverage(score_board[0].scores), 1)
            }
            dataScores.append(dataScore)
    send_email(dataScores, 'Toán', hk)
    return jsonify({'status': 'ok', 'message': 'Data sent successfully'})


@app.route('/chinhsuadiem')
@restrict_to_roles([UserRoleEnum.Teacher], next_url='chinhsuadiem')
def chinhsuadiem():
    funcs = dao.load_function(current_user.user_role)
    currentSchoolYear = app.config['school_year']
    subject = ""
    list_class = []
    kw = request.args.get('kw')
    list_class = dao.getClassesByTeacher(current_user.id, currentSchoolYear, kw)
    subject = dao.getSubjectByUser(current_user.id)
    return render_template("chinhsuadiem.html",
                           subject=subject,
                           list_class=list_class,
                           funcs=funcs)


@app.route('/chinhsuadiem/<int:idLop>', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Teacher], next_url='chinhsuadiem')
def chinhsuadiemLop(idLop):
    currentSchoolYear = app.config['school_year']
    if request.method == 'POST':
        # get all scores
        inputTenLop = request.form.get('inputTenLop')
        inputTenMon = request.form.get('inputTenMon')
        inputHocki = request.form.get('inputHocki')
        score_boards = dao.getScoreBoard(inputTenLop, inputTenMon, inputHocki, currentSchoolYear)
        dataScores = []
        for score_board in score_boards:
            dataScore = {
                'score_board_id': score_board.id,
                '15p': request.form.getlist(f'15p{score_board.id}[]'),
                '45p': request.form.getlist(f'45p{score_board.id}[]'),
                'ck': request.form.get(f'ck{score_board.id}')
            }
            dataScores.append(dataScore)
        dao.update_score(dataScores)
        return redirect(url_for('chinhsuadiem'))

    funcs = dao.load_function(current_user.user_role)
    inputTenLop = dao.getClass(idLop).name
    inputHocki = request.args.get('inputHocki') or 'HK1'
    inputTenMon = dao.getSubjectByUser(current_user.id).name
    score_boards = dao.getScoreBoard(inputTenLop, inputTenMon, inputHocki, currentSchoolYear)
    dataScores = []
    if len(score_boards):
        for score_board in score_boards:
            dataScore = {
                'score_board_id': score_board.id,
                'student_name': score_board.name,
                'student_dob': score_board.dob,
                '15p': [score.value for score in score_board[0].scores if score.type == '15p'],
                '45p': [score.value for score in score_board[0].scores if score.type == '45p'],
                'ck': [score.value for score in score_board[0].scores if score.type == 'ck'][0]
            }
            dataScores.append(dataScore)
    inputCot15p = len(dataScores[0]['15p']) if len(dataScores) else None
    inputCot45p = len(dataScores[0]['45p']) if len(dataScores) else None
    return render_template('chinhsuadiemLop.html', funcs=funcs,
                           idLop=idLop, score_boards=score_boards,
                           inputCot15p=inputCot15p, inputCot45p=inputCot45p,
                           inputTenLop=inputTenLop, inputTenMon=inputTenMon,
                           inputHocki=inputHocki,
                           dataScores=dataScores)


@app.route('/xemdiem')
@restrict_to_roles([UserRoleEnum.Teacher], next_url='xemdiem')
def xemdiem():
    funcs = dao.load_function(current_user.user_role)
    currentSchoolYear = app.config['school_year']
    inputTenMon = dao.getSubjectByUser(current_user.id).name
    semesters = dao.getSemesterTeacher(current_user.id)  # Lấy các học kì 1 ra

    schoolYears = [semester.name.split('_')[1] for semester in semesters]  # lọc lấy niên học
    schoolYears = sorted(schoolYears, key=lambda x: int(x.split('-')[0]), reverse=True)  # sắp xếp niên học giảm dần
    inputNienHoc = request.args.get('inputNienHoc') or schoolYears[0]
    kw = ''
    list_class = dao.getClassesByTeacher(current_user.id, inputNienHoc, kw)
    return render_template("xemdiem.html", funcs=funcs,
                           inputNienHoc=inputNienHoc, schoolYears=schoolYears,
                           list_class=list_class)


@app.route('/xemdiem/<int:idLop>/<int:hk>')
@restrict_to_roles([UserRoleEnum.Teacher], next_url='xemdiem')
def xemdiemlop(idLop, hk):
    funcs = dao.load_function(current_user.user_role)
    tenLop = dao.getClass(idLop).name
    tenMon = dao.getSubjectByUser(current_user.id).name
    semesters = dao.getSemesterByClassId(idLop)
    nienhoc = semesters[0].name.split('_')[1]
    score_boards = dao.getScoreBoardByClass(idLop, current_user.subject_id, f"HK{hk}")
    print(score_boards)

    dataScores = []
    if score_boards and score_boards[0][0].scores:
        for score_board in score_boards:
            dataScore = {
                'score_board_id': score_board.id,
                'student_name': score_board.name,
                'student_dob': score_board.dob,
                '15p': [score.value for score in score_board[0].scores if score.type == '15p'],
                '45p': [score.value for score in score_board[0].scores if score.type == '45p'],
                'ck': [score.value for score in score_board[0].scores if score.type == 'ck'][0],
                'dtb': round(calSemesterAverage(score_board[0].scores), 1)
            }
            dataScores.append(dataScore)
    cot15p = len(dataScores[0]['15p']) if len(dataScores) else 0
    cot45p = len(dataScores[0]['45p']) if len(dataScores) else 0
    return render_template("xemdiemlop.html", funcs=funcs,
                           idLop=idLop, score_boards=score_boards,
                           cot15p=cot15p, cot45p=cot45p,
                           tenLop=tenLop, tenMon=tenMon,
                           hocKi=hk, nienhoc=nienhoc,
                           dataScores=dataScores)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
