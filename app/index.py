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
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/tiepnhanhocsinh')
@restrict_to_roles([UserRoleEnum.Employee])
def tiepNhanHocSinh():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("tiepNhanHocSinh.html", funcs=funcs)


@app.route('/lapdanhsach', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Employee])
def lapDanhSach():
    funcs = []
    students = []
    size = ""
    grade = 10
    maxSize = 40
    currentSchoolYear = '23-24'
    newNameClass = ''
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
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
def dieuChinhDanhSach():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("dieuChinhDanhSach.html", funcs=funcs)


@app.route('/quydinh')
@restrict_to_roles([UserRoleEnum.Admin])
def quyDinh():
    funcs = []

    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("quyDinh.html", funcs=funcs)


@app.route('/thongke')
@restrict_to_roles([UserRoleEnum.Admin])
def thongKe():
    score_min = request.args.get('filterScoreMin')
    score_max = request.args.get('filterScoreMax')
    semester = request.args.get('semester')
    subject = request.args.get('subject')
    classroom = request.args.get('classroom')

    funcs = []

    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("thongKe.html", funcs=funcs,
                           score_stats=dao.scores_stats(scoreMin=score_min, scoreMax=score_max,
                                                        semester=semester,
                                                        subject=subject,
                                                        classroom=classroom),
                           semesters=dao.get_semester(),
                           subjects=dao.get_subject(),
                           classrooms=dao.get_classroom())


@app.route('/nhapdiem', methods=["GET", "POST"])
@restrict_to_roles([UserRoleEnum.Teacher])
def diem():
    semester = 'HK1_23-24'
    if request.method == 'POST':
        #get all scores
        inputTenLop = request.form.get('inputTenLop')
        inputTenMon = request.form.get('inputTenMon')
        score_boards = dao.getScoreBoard(inputTenLop, inputTenMon, semester)
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
        return redirect(url_for('diem'))

    funcs = dao.load_function(current_user.user_role)
    inputTenLop = request.args.get('inputTenLop') or ''
    inputTenMon = request.args.get('inputTenMon') or ''
    maxcot15p = request.args.get('inputCot15p') or '1'
    maxcot45p = request.args.get('inputCot45p') or '1'
    maxcot15p = int(maxcot15p)
    maxcot45p = int(maxcot45p)
    subjects = dao.getAllSubject()
    score_boards = []
    if inputTenLop and inputTenMon and maxcot15p and maxcot45p:
        score_boards = dao.getScoreBoard(inputTenLop, inputTenMon, semester)

    return render_template("diem.html",
                           funcs=funcs, inputTenLop=inputTenLop,
                           maxcot15p=maxcot15p, maxcot45p=maxcot45p,
                           score_boards=score_boards, subjects=subjects,
                           inputTenMon=inputTenMon)


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
    return render_template("chinhsuadiem.html", funcs=funcs)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
