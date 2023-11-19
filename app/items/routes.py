from app.items import bp
from flask import abort, request, jsonify
from werkzeug.exceptions import HTTPException
import json
import sqlite3
from random import randint
from app.db import get_db_connection

# Route to insert items based on store
@bp.route('/', methods=["POST"])
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
        print(e)
    return data


# Route to get item based on store
@bp.route('/<store_id>', methods=["GET"])
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
