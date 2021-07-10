from flask import jsonify, request, Blueprint, current_app
import sqlite3
from datetime import datetime
from app.db_operations.pdf_generation import set_header,set_user_data,table_render,convert_html_to_pdf


miri_module = Blueprint('miri_module', __name__, url_prefix='/miri')

def connect_sqlite():
    con = sqlite3.connect('database.miri')
    return con

def dispose(con):
    con.close()

def _update_db(data):
    print("======>>>>>> >>>>")
    conn = connect_sqlite()
    try:
        cur = conn.cursor()
        for each in data:
            product_info = each['name'].split('/')
            new_count = int(product_info[3])-int(each['count'])
            cur.execute("UPDATE products SET count = ? WHERE id = ?",(new_count, product_info[1]))
            conn.commit()
        return True
    except Exception as e:
        print("---")
        print("--- we got upsert error ----")
        print(e)
        conn.rollback()
        dispose(conn)
        return False


def insert_bills(bill_ref):
    conn = connect_sqlite()

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO bills (bill_ref) VALUES (?)",(bill_ref,))
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        print(e)
        conn.rollback()
        dispose(conn)
        return False



@miri_module.route('/fetch_products',methods=['GET'])
def fetch_products():
    return jsonify({'message':"success"}),200

@miri_module.route('/create/db',methods=['GET'])
def create_products():
    conn = connect_sqlite()
    try:
        print("here")
        try:
            conn.execute("DROP TABLE ventors")
            conn.execute("DROP TABLE products")
            conn.execute("DROP TABLE bills")
        except Exception as e:
            print(e)
            print("Db not found")
        upsert = f"CREATE TABLE ventors (ID INTEGER PRIMARY KEY  autoincrement ,name TEXT, ventor_id TEXT, ventor_desc TEXT, gst_number TEXT)"
        conn.execute(upsert)
        upsert = f"CREATE TABLE products (ID INTEGER PRIMARY KEY    autoincrement ,name TEXT, HSN_SAC TEXT, ventor_name TEXT, cost TEXT,count INTEGER)"
        conn.execute(upsert)
        upsert = f"CREATE TABLE bills (ID INTEGER PRIMARY KEY    autoincrement ,bill_ref TEXT)"
        conn.execute(upsert)
        return jsonify({'message':"success"}),200
    except Exception as e:
        print(e)
        return jsonify({'status':'failed'}),403
    finally:
        dispose(conn)

@miri_module.route('/insert',methods=['POST'])
def insert_products():
    conn = connect_sqlite()
    try:
        payload = request.json
        data = payload.get('upsert_data')
        cur = conn.cursor()
        print(data)

        if payload['type'] == "ventors":
            cur.execute("INSERT INTO ventors (name,ventor_id,ventor_desc,gst_number) VALUES (?,?,?,?)",
                        (data['name'],data['ventor_id'],data['desc'],data['gst_number']))
        else:
            print("-----")
            cur.execute("INSERT INTO products (name,HSN_SAC,ventor_name,cost,count) VALUES (?,?,?,?,?)",
                        (data['name'], data['code'], data['ventor'], data['cost'],data['count']))
        conn.commit()
        return jsonify({'message':"success"}),200
    except Exception as e:
        conn.rollback()
        print(e)
        return jsonify({'status':'failed'}),403
    finally:
        dispose(conn)

@miri_module.route('/fetch_ventors',methods=['GET'])
def fetch_ventors():
    con = connect_sqlite()
    try:
        cur = con.cursor()
        cur.execute("SELECT name FROM ventors")  # execute a simple SQL select query
        ventors =[x[0] for x in cur.fetchall()]
        print(ventors)
        return jsonify({'message': "success",'result':ventors}), 200
    except Exception as e:
        print(e)
        con.rollback()
        return jsonify({'status': 'failed'}), 403
    finally:
        dispose(con)

@miri_module.route('/bill_generation',methods=['POST'])
def bill_generation():

    try:
        data = request.json
        html = set_header(123)
        html = set_user_data(html, data['user_data'])
        html = table_render(html, data['oders'])
        file_name = f"pdf_store/miRi_bill_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.pdf"
        convert_html_to_pdf(html, file_name)
        print("---- ---- >>> HERE")
        _id = insert_bills(file_name)
        print(_id)
        if not _id:
            raise Exception('Failed upsert')

        if not _update_db(data['oders']):
            print("failed -- upsert")
            raise Exception('Failed upsert')

        return jsonify({'status':'success','file_link':file_name,'bill_ref':str(_id)})
    except Exception as e:
        return jsonify({'status':'failed','message':'failed to generate bill'})


@miri_module.route('/products/query',methods=['GET'])
def product_search():
    con = connect_sqlite()
    try:
        cur = con.cursor()
        data = request.args.get('query')
        print(data)
        var = cur.execute("SELECT * FROM products WHERE name LIKE (?)", ('%'+data+'%',))
        products = []
        for each in var:
            products.append(f"{str(each[1])} /{each[0]}/{each[2]}/{each[5]}")
        return jsonify({'status':'success','products':products})
    except Exception as e:
        print(e)
        con.rollback()
        return jsonify({'status': 'failed'}), 403
    finally:
        dispose(con)

