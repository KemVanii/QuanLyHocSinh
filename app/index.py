from flask import Flask, render_template
from app import app, db
import dao
app = Flask(__name__)


@app.route('/')
def index():
    cates = dao.load_categories()
    return render_template('index.html',categories=cates)


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
