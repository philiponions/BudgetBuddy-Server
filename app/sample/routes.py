from app.sample import bp
from flask import abort, request, jsonify
from werkzeug.exceptions import HTTPException
import json
import sqlite3
from random import randint
from app.db import get_db_connection


# Route to insert users
@bp.route('/user', methods=["POST"])
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
@bp.route('/user/login', methods=["POST"])
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
        conn.commit()
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


# Route to insert store
@bp.route('/store', methods=["POST"])
def store_post():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        data = request.get_json()
        user_name = data["username"]
        store_name = data["name"]
        data = store_name

        # Establish the connection and insert into database
        conn = get_db_connection()

        count = conn.execute(
            'SELECT COUNT(*) FROM stores WHERE username = ?;', (user_name,)).fetchall()
        if count[0][0] != 1:
            return "Invalid"

        # See if the store already exists
        count = conn.execute(
            'SELECT COUNT(*) FROM stores WHERE name LIKE ? and username = ?;', ('%' + store_name + '%', user_name)).fetchall()
        if count[0][0] == 1:
            return "Store already added"

        # Generate random store id
        is_valid_number = False
        while not is_valid_number:
            store_id = randint(1, 10000)
            count = conn.execute(
                'SELECT COUNT(*) FROM stores where store_id = ?;', (store_id,)).fetchall()

            # Check if the store_id already exists
            if count[0][0] == 0:
                is_valid_number = True
                break

        try:
            query = "INSERT INTO stores (store_id, name, username) VALUES (?,?,?)"

            conn.execute(query, (store_id, store_name, user_name))
            conn.commit()
            conn.close()

            data = "Inserted store successfully"
        except Exception as e:
            data = "Failed to insert store" + str(e)

    except Exception as e:
        print(e)
        data = str(e)
    return data


# Route to get store
@bp.route('/store/', methods=["GET"])
def store_get():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        data = request.get_json()
        user_name = data["username"]
        store_name = data["name"]
        store_id = data["store_id"]

        # Establish the connection and insert into database
        conn = get_db_connection()

        query = "SELECT COUNT(*) FROM stores WHERE username = ? and store_id = ?"

        count = conn.execute(query, (user_name, store_id)).fetchall()
        conn.commit()
        conn.close()
        if count[0][0] == 1:
            data = "Store found " + store_name
        elif count[0][0] == 0:
            data = "No store added"
        else:
            data = "Error in checking store" + store_name

    except Exception as e:
        print(e)
        data = str(e)
    return data


# Route to insert items based on store
@bp.route('/items', methods=["POST"])
def items_post():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        data = request.get_json()
        item_name = data["item_name"]
        store_name = data["name"]
        store_id = data["store_id"]

        # Establish the connection and insert into database
        conn = get_db_connection()

        # Generate random store id
        is_valid_number = False
        while not is_valid_number:
            item_id = randint(1, 10000)
            try:
                count = conn.execute(
                    'SELECT COUNT(*) FROM items where item_id = ? and store_id = ?;', (item_id, store_id,)).fetchall()
            except Exception as e:
                return e
            # Check if the store_id already exists
            if count[0][0] == 0:
                is_valid_number = True
                break

        try:
            query = "INSERT INTO items (item_id, item_name, store_id) VALUES (?,?,?)"

            conn.execute(query, (item_id, item_name, store_id))
            conn.commit()
            conn.close()

            data = "Inserted item successfully " + item_name + " " + store_name
        except Exception as e:
            data = "Failed to insert item" + str(e)

    except Exception as e:
        print("Here")

    return data


# Route to get item based on store
@bp.route('/items/<store_id>', methods=["GET"])
def item_get(store_id):
    data = ""
    try:
        # Get the store_id from the URL parameter
        # Retrieve data from the request's JSON body

        # Establish the connection and insert into database
        conn = get_db_connection()

        query = "SELECT item_name FROM items WHERE store_id = ?"

        data = conn.execute(query, (store_id,)).fetchall()
        conn.commit()
        conn.close()
        if data and len(data) > 0:
            # Extract item names from the fetched data
            item_names = [item[0] for item in data]
            response = jsonify(item_names=item_names)
            # Set content type to JSON
            response.headers['Content-Type'] = 'application/json'
            return response, 200  # Return item names directly in the response body
        else:
            response = jsonify(message="No items found for this store")
            # Set content type to JSON
            response.headers['Content-Type'] = 'application/json'
            return response, 404  # Return a message if no items are found

    except Exception as e:
        print(e)
        data = str(e)
    return data
