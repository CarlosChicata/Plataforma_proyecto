import sqlite3


CONN = sqlite3.connect('main.db', check_same_thread=False)
cur = CONN.cursor()


def generateTable():
    cur.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text null,
                lastname text null,
                username text null,
                password text null,
                deleted boolean default false,
                login boolean default false null
            )
        ''')
    cur.execute('''
            CREATE TABLE product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_image_inner text null,
                name text null,
                description text null,
                quantity integer default 0 NULL,
                mimetype text null
            )
        ''')
    cur.execute('''
            CREATE TABLE compra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id integer default 0 NULL,
                cost real default 0.0 NULL,
                status integer default 0
            )
        ''')
    cur.execute('''
            CREATE TABLE compra_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id integer default 0 NULL,
                product_id integer default 0 NULL,
                quantity integer default 0 NULL
            )
        ''')

def removerProductoCompra(cid, pid):
    query = '''
            DELETE FROM compra_item WHERE compra_id = %s AND product_id= %s 
        ''' % (cid, pid, )
    cur.execute(query)
    CONN.commit()
    return 



def getInfoProductByCompra(id):
    rpta= False
    query = '''
        select p.name, 
            p.description,
            p.id, 
            p.quantity, 
            coi.id, 
            co.id
        from compra co
        join compra_item coi
            on co.id = coi.compra_id
        join product p
            on p.id = coi.product_id
        where co.id = %s
    ''' % (id,)
    users = []
    for row in cur.execute(query):
        rpta = True
        print(row)
        users.append(row)
    return rpta, users


def insertCompraItem(cid, pid, cantidad):
    query = '''
            INSERT INTO compra_item (compra_id,product_id,quantity) VALUES (%s,%s,%s)
        ''' % (cid, pid, cantidad,)
    cur.execute(query)
    CONN.commit()
    return 


def getItemByCompra(id):
    rpta = False
    query = '''
        SELECT * FROM compra_item WHERE compra_id = %s
        ''' % (id,)
    users = []
    for row in cur.execute(query):
        rpta = True
        print(row)
        users.append(row)
    return rpta, users    


def cerrarCompra(id, flag):
    rpta, users = getCompra(id)
    print(users)
    if len(users) != 1:
        return False, "No son credenciales adecuadas"
    elif users[0][0] is None:
        return False, "No es registrado correctamente"
    else:
        query = '''
                UPDATE compra
                SET status = %s
                where id = %s
            ''' % (flag, users[0][0])
        #print(query)
        cur.execute(query)
        CONN.commit()
        return True, ""


def getCompra(id):
    rpta = False
    query = '''
        SELECT * FROM compra WHERE id = "%s"
        ''' % (id,)
    users = []
    for row in cur.execute(query):
        rpta = True
        print(row)
        users.append(row)
    return rpta, users


def getCompraByUser(id):
    rpta = False
    query = '''
        SELECT * FROM compra WHERE user_id = "%s"
        ''' % (id,)
    users = []
    for row in cur.execute(query):
        rpta = True
        print(row)
        users.append(row)
    return rpta, users


def insertCompra(id):
    query = '''
            INSERT INTO compra (user_id) VALUES (%s)
        ''' % (id,)
    cur.execute(query)
    CONN.commit()
    return 


def getAllCompraByUSer(id):
    rpta = False
    query = '''
        SELECT * FROM compra WHERE user_id = %s AND status = 0
        ''' % (id,)
    users = []
    for row in cur.execute(query):
        rpta = True
        print(row)
        users.append(row)
    return rpta, users


def getUser(username, password):
    rpta = False
    query = '''
        SELECT * FROM user WHERE password = "%s" AND username = "%s"
        ''' % (password,username,)
    users = []
    for row in cur.execute(query):
        rpta = True
        print(row)
        users.append(row)
    return rpta, users


def insertUser(name, lastname, username, password):
    query = '''
            INSERT INTO user (name, lastname, username, password) VALUES ("%s","%s","%s","%s")
        ''' % (name, lastname, username, password)
    cur.execute(query)
    CONN.commit()
    return 


def logUserSystem(username, password, flag):
    rpta, users = getUser(username, password)
    print(users)
    if len(users) != 1:
        return False, "No son credenciales adecuadas"
    elif users[0][0] is None:
        return False, "No es registrado correctamente"
    else:
        query = '''
                UPDATE user
                SET login = %s
                where id = %s
            ''' % (flag, users[0][0])
        #print(query)
        cur.execute(query)
        CONN.commit()
        return True, ""


def getProduct(id):
    rpta = False
    query = '''
        SELECT * FROM product WHERE id = "%s"
        ''' % (id,)
    users = []
    for row in cur.execute(query):
        rpta = True
        print(row)
        users.append(row)
    return rpta, users


def getAllProduct():
    rpta = False
    query = '''
        SELECT * FROM product
        '''
    users = []
    for row in cur.execute(query):
        rpta = True
        print(row)
        users.append(row)
    return rpta, users


def addOneProduct(url_image_inner,name,description,quantity, mimetype):
    query = '''
            INSERT INTO product (url_image_inner,name,description,quantity,mimetype) VALUES  ("%s","%s", "%s",%s,"%s")
        ''' % (url_image_inner,name,description,quantity,mimetype,)
    rpta = cur.execute(query)
    #print(rpta)
    CONN.commit()
    return 



