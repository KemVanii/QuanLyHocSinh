import hashlib

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from flask_login import login_user, logout_user, current_user
from app import app, login
from app.models import *
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
def tiepNhanHocSinh():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("tiepNhanHocSinh.html", funcs=funcs)


@app.route('/lapdanhsach', methods=["GET", "POST"])
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
            dao.createNewClassGrade10(newNameClass,size,grade,currentSchoolYear)
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
def dieuChinhDanhSach():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("dieuChinhDanhSach.html", funcs=funcs)


@app.route('/quydinh')
def quyDinh():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("quyDinh.html", funcs=funcs)


@app.route('/thongke')
def thongKe():
    score_min = request.args.get('filterScoreMin')
    score_max = request.args.get('filterScoreMax')
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("thongKe.html", funcs=funcs,
                           score_stats=dao.scores_stats(scoreMin=score_min, scoreMax=score_max))


@app.route('/nhapdiem', methods=["GET", "POST"])
def diem():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("diem.html", funcs=funcs)


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


def nhap_diem():
    tenLop = String(request.form.get("inputTenLop"))
    maxcot15p = int(request.form.get("inputCot15p"))
    maxcot45p = int(request.form.get("inputCot45p"))
    tenMon = String(request.form.get("inputTenMon"))
    Lops = db.session.query(Class).all()
    Students = db.session.query(Student).all()
    Hocki = 'nkncifiitjm'
    score_boards=[]

    for lop in Lops:
        if (lop.name == tenLop):
            for ssb in lop.score_boards:
                # diem[ssb.student_id] ds diem cua hoc sinh
                # diem[ssb.student_id]['15p']
                for i in range(0, maxcot15p):
                    u = Score(value=diem[ssb.student_id]['15p'][i], type='15p', score_boards=ssb.id)
                for i in range(0, maxcot15p):
                    u = Score(value=diem[ssb.student_id]['15p'][i], type='15p', score_boards=ssb.id)
                    db.session.add(u)
                for i in range(0, maxcot45p):
                    u = Score(value=diem[ssb.student_id]['45p'][i], type='45p', score_boards=ssb.id)
                    db.session.add(u)
                u = Score(value=diem[ssb.student_id]['CK'], type='CK', score_boards=ssb.id)
                db.session.add(u)
                db.session.commit()
        if request.method == "POST":
            score_boards = dao.getScoreBoard(tenLop,tenMon,Hocki)



@app.route('/chinhsuadiem')
def chinhsuadiem():
    funcs = []
    if current_user.is_authenticated:
        funcs = dao.load_function(current_user.user_role)
    return render_template("chinhsuadiem.html", funcs=funcs)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
