from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = '18sdjksdgjs&%^&^(*@@*#&@#^@DGGHJHG'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/quanlyhocsinh?charset=utf8mb4" % quote(
    'Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
# app.config["maxClassSize"] = int(dao.readjson()['maxClassSize'])


db = SQLAlchemy(app=app)
login = LoginManager()
login.init_app(app)

