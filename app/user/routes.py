from app.user import bp
from flask import abort, request
from werkzeug.exceptions import HTTPException
import json
import sqlite3
from app.db import get_db_connection


# Route to insert users
@bp.route('/', methods=["POST"])
def user_post():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        data = request.get_json()
        user_name = data["username"]
        password = data["password"]
        data = password

        # Establish the connection and insert into database
        conn = get_db_connection()

        query = "INSERT INTO users (username, password) VALUES (?,?)"

        conn.execute(query, (user_name, password))
        conn.commit()
        conn.close()

        data = "Success"

    except Exception as e:
        print(e)
        data = str(e)
    return data


# Route to get user
@bp.route('/login', methods=["POST"])
def user_get():
    data = ""
    try:
        data = request.get_json()
        username = data["username"]
        # Retrieve data from the request's JSON body
        password = data["password"]

        # Establish the connection and insert into database
        conn = get_db_connection()

        query = "SELECT COUNT(*) from users where username = ? and password = ?"

        count = conn.execute(query, (username, password)).fetchall()
        conn.close()
        if count[0][0] == 1:
            data = "User found"
        elif count[0][0] == 0:
            data = "No User Found"
        else:
            data = "Error in checking user"

    except Exception as e:
        print(e)
        data = str(e)
    return data