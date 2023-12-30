import hashlib

from flask import Flask, render_template, request, redirect, url_for
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

    print(funcs)
    return render_template('index.html', funcs=funcs)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == str(hashlib.md5(request.form.get("pswd").encode('utf-8')).hexdigest()):
            login_user(user)
            return redirect(url_for("index"))

    return render_template("login.html")
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
