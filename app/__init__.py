from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
import os

app = Flask(__name__)

app.secret_key = '18sdjksdgjs&%^&^(*@@*#&@#^@DGGHJHG'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/quanlyhocsinh?charset=utf8mb4" % quote(
    'admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True

json_file_path = os.path.join(app.root_path, 'static', 'policies.json')
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Update app.config with data from the JSON file
for key, value in data.items():
    app.config[key] = value

db = SQLAlchemy(app=app)
login = LoginManager()
login.init_app(app)
