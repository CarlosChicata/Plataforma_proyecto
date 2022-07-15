from flask import Flask
from flask import request, send_file

import sqlite3
from datetime import datetime
import os
import pathlib
from DB import generateTable, getUser, insertUser, logUserSystem, addOneProduct, \
    getAllProduct, getProduct, getAllCompraByUSer, insertCompra, cerrarCompra, \
    getCompra, insertCompraItem, getItemByCompra, getCompraByUser, getInfoProductByCompra, \
    removerProductoCompra

app = Flask(__name__)


generateTable()


@app.route("/login", methods=[ 'POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if password is None or username is None:
        return { "error": "Le falta usuario o password"}
    else:
        flag, rpta = logUserSystem(username, password, True)
        if flag == False:
            return {"error": "no es valido", "status": False}
        else:
            return {"status": True}


@app.route("/logout", methods=[ 'POST'])
def logout():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if password is None or username is None:
        return { "error": "Le falta usuario o password"}
    else:
        flag, rpta = logUserSystem(username, password, False)
        if flag == False:
            return {"error": "no es valido", "status": False}
        else:
            return {"status": True}


@app.route("/insert/user", methods=["POST"])
def addUser():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    lastname = data.get("lastname")
    name = data.get("name")
    if name is None or lastname is None or password is None or username is None :
        return {"status": False, "error": "Falta datos"}
    else:
        insertUser(name, lastname, username, password)
        rpta, users = getUser(username, password)
        return {"status": rpta}


@app.route("/insert/product", methods=["POST"])
def addProduct():
    try:
        image = request.files.get("image")
        name = request.form.get("name"),
        description = request.form.get("description"),
        quantity = int(request.form.get("quantity"))
        folder = pathlib.Path(__file__).parent.resolve()
        folder = "."
        filename = os.path.join(folder, "images", image.filename)
        image.save(filename)

        addOneProduct(filename,name,description,quantity, image.mimetype)
        getAllProduct()
        return {"status": True}
    except Exception as e:
        print(e)
        return {"status": False, "error": str(e)}


@app.route("/products", methods=["POST", "GET"])
def showAllProduct():
    rpta = []
    flag, products = getAllProduct()
    for item in products:
        #print(item)
        rpta.append({
            "description": item[3],
            "id": item[0],
            "name": item[2],
            "quantity": int(item[4]),
        })
        print(item)
    return {
        "data": rpta
    }


@app.route("/product/image/<id>", methods=["POST", "GET"])
def productImage(id):
    flag, info = getProduct(id)
    if len(info) != 1:
        return {"error": "no es exacto"}
    else:
        return send_file(info[0][1],mimetype= info[0][5])


@app.route("/insert/compra", methods=["POST"])
def createCompra():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if password is None or username is None:
        return { "error": "Le falta usuario o password"}

    else:
        flag, user = getUser(username, password)
        if len(user) == 0: return {"error": "no esta definido el usuario"}
        else:
            id = user[0][0]
            insertCompra(id)
            getAllCompraByUSer(id)
            return {"status": True}

@app.route("/cerrar/compra/<id>", methods=["POST"])
def closeCompra(id):
    flag, msg = cerrarCompra(id, 1)
    getCompra(id)
    if flag is False:
        return {"status": False, "error": msg}
    else:
        return {"status": True}


@app.route("/agregar/compra/producto", methods=["POST"])
def addProductoCompra():
    data = request.json
    product_id = data.get("product_id")
    compra_id = data.get("compra_id")
    quantity = int(data.get("quantity"))

    if quantity is None or product_id is None or compra_id is None:
        return {"status": False}
    else:
        insertCompraItem(compra_id,product_id,quantity)
        getItemByCompra(compra_id)
        return {"status": True}


@app.route("/compras", methods=["POST"])
def infoCompra():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if password is None or username is None:
        return { "error": "Le falta usuario o password"}

    else:
        flag, user = getUser(username, password)
        if len(user) == 0: return {"error": "no esta definido el usuario"}
        else:
            rpta = []
            id = user[0][0]
            flag, compras = getCompraByUser(id)
            for compra in compras:
                solicitud = { "id_compra": compra[0]}
                productos = []
                flag, items = getInfoProductByCompra(compra[0])
                for item in items:
                    productos.append({
                        "id_item": item[4],
                        "description": item[1],
                        "id": item[2],
                        "name": item[0],
                        "quantity": int(item[3]),
                    })
                solicitud["productos"] = productos
                rpta.append(solicitud)

            return {"status": True, "data": rpta}


@app.route("/eliminar/compra/producto", methods=["POST"])
def removeProductoCompra():
    data = request.json
    product_id = data.get("product_id")
    compra_id = data.get("compra_id")

    if product_id is None or compra_id is None:
        return {"status": False}
    else:
        removerProductoCompra(compra_id,product_id)
        #getItemByCompra(compra_id)
        return {"status": True}



if __name__ == '__main__':
   app.run()
   print("salimos")