from flask import Flask
from flask import render_template, request

from datetime import datetime


app = Flask(__name__)


DB = dict()
DB_key = dict()


@app.route("/")
def index():
    for key, value in DB.items():
        if DB[key]["login"]:
            return render_template("main.html", name=DB[key]["fullname"])
    else: return render_template("index.html")


@app.route("/<variable>/operation", methods=['GET', 'POST'])
def operation(variable):
    if variable == 'login':
        return render_template("login.html")
    elif variable == 'signin':
        return render_template("signIn.html")
    else:
        return render_template("index.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    nickname = request.form.get("nickname")
    key = DB_key.get(nickname, None)
    value = DB.get(key, None)
    value["login"] = False
    DB[key] = value
    return render_template("index.html")



@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    key = "\n".join([password, username])
    value = DB.get(key, None)
    if value is None:
        return render_template("login.html", error="No es correcto")
    else:
        value["login"] = True
        DB[key] = value
        return render_template("main.html", name=value["fullname"])


@app.route("/register", methods=['GET', 'POST'])
def register():
    fullname = request.form.get("fullname")
    username = request.form.get("username")
    password = request.form.get("password")
    key = "\n".join([password,username])
    DB_key[fullname] = key
    DB[key] = {
        "fullname": fullname,
        "username": username,
        "password": password,
        "login": False,
    }
    return render_template("login.html")
