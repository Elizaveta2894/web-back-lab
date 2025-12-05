from flask import Blueprint, render_template, request, session, current_app
import json
from os import path
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3

lab6 = Blueprint('lab6', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='liza_stabrovskaya_knowledge_base',
            user='liza_stabrovskaya_knowledge_base',
            password='555'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


def init_offices_table():
    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT COUNT(*) as count FROM offices;")
        else:
            cur.execute("SELECT COUNT(*) as count FROM offices;")
        
        result = cur.fetchone()
        
        if result['count'] == 0:
            for i in range(1, 11):
                number = i
                price = 900 + i * 100
                
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute(
                        "INSERT INTO offices (number, price) VALUES (%s, %s);",
                        (number, price)
                    )
                else:
                    cur.execute(
                        "INSERT INTO offices (number, price) VALUES (?, ?);",
                        (number, price)
                    )
        
        db_close(conn, cur)
    except Exception as e:
        print(f"Error initializing offices table: {e}")


@lab6.route('/lab6/')
def main():
    init_offices_table()
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    method = data.get('method')
    request_id = data.get('id')
    
    if method == 'info':
        try:
            conn, cur = db_connect()
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
            else:
                cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
            
            offices_data = cur.fetchall()
            
            offices_list = []
            for office in offices_data:
                offices_list.append({
                    "number": office['number'],
                    "tenant": office['tenant'] if office['tenant'] else "",
                    "price": office['price']
                })
            
            db_close(conn, cur)
            
            return {
                "jsonrpc": "2.0",
                "result": offices_list,
                "id": request_id
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": f"Database error: {str(e)}"
                },
                "id": request_id
            }
    
    elif method == 'booking':
        login = session.get('login')
        if not login:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 1,
                    "message": "Unauthorized"
                },
                "id": request_id
            }

        office_number = data.get('params')
        
        try:
            conn, cur = db_connect()
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute(
                    "SELECT tenant FROM offices WHERE number = %s;",
                    (office_number,)
                )
            else:
                cur.execute(
                    "SELECT tenant FROM offices WHERE number = ?;",
                    (office_number,)
                )
            
            office = cur.fetchone()
            
            if not office:
                db_close(conn, cur)
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 4,
                        "message": "Office not found"
                    },
                    "id": request_id
                }
            
            if office['tenant']:
                db_close(conn, cur)
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 2,
                        "message": "Office already booked"
                    },
                    "id": request_id
                }
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute(
                    "UPDATE offices SET tenant = %s WHERE number = %s;",
                    (login, office_number)
                )
            else:
                cur.execute(
                    "UPDATE offices SET tenant = ? WHERE number = ?;",
                    (login, office_number)
                )
            
            db_close(conn, cur)
            
            return {
                "jsonrpc": "2.0",
                "result": "success",
                "id": request_id
            }
            
        except Exception as e:
            if 'conn' in locals() and 'cur' in locals():
                db_close(conn, cur)
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": f"Database error: {str(e)}"
                },
                "id": request_id
            }
    
    elif method == 'cancellation':
        login = session.get('login')
        if not login:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 1,
                    "message": "Unauthorized"
                },
                "id": request_id
            }
        
        office_number = data.get('params')
        
        try:
            conn, cur = db_connect()

            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute(
                    "SELECT tenant FROM offices WHERE number = %s;",
                    (office_number,)
                )
            else:
                cur.execute(
                    "SELECT tenant FROM offices WHERE number = ?;",
                    (office_number,)
                )
            
            office = cur.fetchone()
            
            if not office:
                db_close(conn, cur)
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 4,
                        "message": "Office not found"
                    },
                    "id": request_id
                }
            
            if office['tenant'] != login:
                db_close(conn, cur)
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": 3,
                        "message": "Cannot cancel other user's booking"
                    },
                    "id": request_id
                }
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute(
                    "UPDATE offices SET tenant = '' WHERE number = %s;",
                    (office_number,)
                )
            else:
                cur.execute(
                    "UPDATE offices SET tenant = '' WHERE number = ?;",
                    (office_number,)
                )
            
            db_close(conn, cur)
            
            return {
                "jsonrpc": "2.0",
                "result": "success",
                "id": request_id
            }
            
        except Exception as e:
            if 'conn' in locals() and 'cur' in locals():
                db_close(conn, cur)
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": f"Database error: {str(e)}"
                },
                "id": request_id
            }
    
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": -32601,
            "message": "Method not found"
        },
        "id": request_id
    }


@lab6.route('/lab6/reset-offices')
def reset_offices():
    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant = '';")
        else:
            cur.execute("UPDATE offices SET tenant = '';")
        
        db_close(conn, cur)
        return "All offices have been reset"
    except Exception as e:
        return f"Error resetting offices: {str(e)}"