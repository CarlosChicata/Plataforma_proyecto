from flask import Flask
from flask import render_template, request

from datetime import datetime
import os
import pathlib


app = Flask(__name__)


#DB = dict()
DB = {
    'cfc12575\nC2': {
        'fullname': 'C2', 
        'username': 'Carlos Fernando Chicata Farfan', 
        'password': 'cfc12575', 
        'login': True
    }
}
DB_key = {
    "C2": 'cfc12575\nC2'
}
DB_product = [
    {
        'description': 'meme', 
        'name': 'meme', 
        'price': '123', 
        'file': './static/Surprise.jpeg'
    },
    {
        'description': 'Producto 1', 
        'name': 'Carlos Fernando', 
        'price': 'casd', 
        'file': './static/fullVoter.png'
    },
    {
        'description': 'Producto 2', 
        'name': 'Carlos Fernando', 
        'price': 'casd', 
        'file': './static/emptyVOter.png'
    }
]



@app.route("/")
def index():
    for key, value in DB.items():
        if DB[key]["login"]:
            return render_template("main.html", name=DB[key]["fullname"], products=DB_product)
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
    print(nickname)
    key = DB_key.get(nickname, None)
    value = DB.get(key, None)
    print(value)
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
        return render_template("main.html", name=value["fullname"], products=DB_product)


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


@app.route("/register-product", methods=['GET', "POST"])
def formProduct():
    return render_template("productForm.html")


@app.route("/upload-product", methods=["POST"])
def uploadProduct():
    # start
    folder = pathlib.Path(__file__).parent.resolve()
    folder = "."
    file = request.files["image"]
    paramsForm = {
        "description": request.form.get("description") or "",
        "name": request.form.get("name") or "",
        "price": request.form.get("price") or "",
        "file": os.path.join(".", "static",file.filename),
    }
    file.save(os.path.join(folder, "static",file.filename))
    DB_product.append(paramsForm)
    # end
    for key, value in DB.items():
        if DB[key]["login"]:
            return render_template("main.html", name=DB[key]["fullname"], products=DB_product)
    else: return render_template("index.html")