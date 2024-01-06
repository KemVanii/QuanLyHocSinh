import hashlib

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from flask_login import login_user, logout_user, current_user
from app import app, login
from app.models import *
from app.auth import restrict_to_roles
import dao


@login.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    else:
        return redirect(url_for('login'))
    return render_template('index.html', funcs=funcs)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        if user and user.password == str(hashlib.md5(request.form.get("pswd").encode('utf-8')).hexdigest()):
            login_user(user)
            next_url = request.form.get("next_url")
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
    funcs = dao.load_function(current_user.user_role)
    return render_template("tiepNhanHocSinh.html", funcs=funcs)


@app.route('/lapdanhsach', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Employee], next_url='lapdanhsach')
def lapdanhsach():
    funcs = dao.load_function(current_user.user_role)
    students = []
    size = ""
    grade = 10
    maxSize = 40
    currentSchoolYear = '23-24'
    newNameClass = ''
    if request.method == "POST":
        action = request.form.get("action")
        size = int(request.form.get("inputSize"))
        grade = int(request.form.get("inputGrade"))
        newNameClass = f'{grade}/{len(dao.getClassByGradeAndSchoolYear(grade, currentSchoolYear)) + 1}'
        if (action == 'xacnhanlap'):
            dao.createNewClassGrade10(newNameClass, size, grade, currentSchoolYear)
            return redirect(url_for('lapDanhSach'))
        else:
            if grade == 10:
                students = dao.getStudentsNotInClass(size)
            if grade == 11 or grade == 12:
                pass
    return render_template("lapDanhSach.html",
                           funcs=funcs, students=students,
                           size=size, grade=grade,
                           maxSize=maxSize, currentSchoolYear=currentSchoolYear,
                           newNameClass=newNameClass)


@app.route('/dieuchinhdanhsach')
@restrict_to_roles([UserRoleEnum.Employee])
def dieuchinhdanhsach():
    funcs = dao.load_function(current_user.user_role)
    currentSchoolYear = '23-24'
    grades = dao.get_grade()
    inputGrade = request.args.get('inputGrade') or 10
    classes = dao.getClassByGradeAndSchoolYear(inputGrade, currentSchoolYear)
    return render_template("dieuChinhDanhSach.html",
                           funcs=funcs, grades=grades,
                           inputGrade=inputGrade, classes=classes)


@app.route('/dieuchinhdanhsach/<int:idLop>', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Employee])
def dieuchinhdanhsachlop(idLop):
    currentSchoolYear = '23-24'
    if request.method == 'POST':
        action = request.form.get('action')
        studentId = request.form.get('student_id')
        if action == 'delete':
            dao.deleteStudentInClass(studentId, idLop, currentSchoolYear)
        return redirect(url_for('dieuchinhdanhsachlop', idLop=idLop))
    funcs = dao.load_function(current_user.user_role)

    grades = dao.get_grade()
    inputGrade = request.args.get('inputGrade') or 10
    cla = dao.getClassById(idLop)
    students = dao.getStudentListByClassId(idLop)
    return render_template("dieuChinhDanhSachlop.html",
                           funcs=funcs, grades=grades,
                           inputGrade=inputGrade, students=students,
                           cla=cla, idLop=idLop)


@app.route('/quydinh')
@restrict_to_roles([UserRoleEnum.Admin])
def quydinh():
    funcs = dao.load_function(current_user.user_role)
    return render_template("quyDinh.html", funcs=funcs)


@app.route('/thongke', methods=["GET"])
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
                           types_stats=dao.types_stats(classroom=classroom_pie, grade=grade_pie),
                           semesters=dao.get_semester(),
                           subjects=dao.get_subject(),
                           classrooms=dao.get_classroom(),
                           grades=dao.get_grade())


@app.route('/nhapdiem', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Teacher])
def nhapdiem():
    currentSchoolYear = '23-24'
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
        "age_max": data.get('age_max')
    }

    session['policies'] = policies

    with open("static/policies.json", "w") as outfile:
        json.dump(policies, outfile)

    return jsonify(policies)


@app.route('/chinhsuadiem')
@restrict_to_roles([UserRoleEnum.Teacher])
def chinhsuadiem():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    subject = ""
    list_class = []
    kw = request.args.get('kw')
    list_class = dao.getClassesByTeacher(current_user.id, kw)
    subject = dao.getSubjectByUser(current_user.id)
    return render_template("chinhsuadiem.html",
                           subject=subject,
                           list_class=list_class,
                           funcs=funcs)


@app.route('/chinhsuadiem/<int:idLop>')
@restrict_to_roles([UserRoleEnum.Teacher])
def chinhsuadiemLop(idLop):
    currentSchoolYear = '23-24'
    funcs = dao.load_function(current_user.user_role)
    inputHocki = request.args.get('inputHocki') or 'HK1'
    inputTenMon = dao.getSubjectByUser(current_user.id).name
    score_boards_sua = dao.getScoreBoard(dao.getClass(idLop).name, inputTenMon, inputHocki, currentSchoolYear)
    inputCot15p = 1
    inputCot45p = 1
    return render_template('chinhsuadiemLop.html', funcs=funcs,
                           idLop=idLop, score_boards_sua=score_boards_sua,
                           inputCot15p=inputCot15p, inputCot45p=inputCot15p)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
