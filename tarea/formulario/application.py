from flask import Flask
from flask import render_template, request

from datetime import datetime


app = Flask(__name__)


DB = set()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello", methods=["POST"])
def login():
    fullname = request.form.get("fullname")
    nickname = request.form.get("nickname")
    birthday = request.form.get("birthday")
    creation_date = datetime.now().strftime('%Y-%m-%d, %H:%M')
    age = request.form.get("age")
    #= request.form.get("")
    return render_template(
        "session.html",
        fullname=fullname,
        creation_date = creation_date,
        nickname = nickname,
        birthday={"birthday": birthday},
        age=age
    )


@app.route("/<string:name>")
def session(name):
    return render_template("session.html", name=name)


@app.route("/user")
def user():
    users= ["Carlitos", "Jessica", "Diana", "Miguel"]
    return render_template("users.html", users=users)
