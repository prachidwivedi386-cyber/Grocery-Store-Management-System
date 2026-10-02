from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_connection import get_sql_connection
import json
import traceback
import  mysql.connector

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)
CORS(app)

# Database connection
try:
    connection = get_sql_connection()
    print("Database Connected Successfully")
except Exception as e:
    print("Database Connection Failed")
    print(e)
    connection = None


@app.route("/")
def home():
    return "Flask Server is Running"


@app.route("/getUOM", methods=["GET"])
def get_uom():
    try:
        response = uom_dao.get_uoms(connection)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/getProducts", methods=["GET"])
def get_products():
    try:
        response = products_dao.get_all_products(connection)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/insertProduct", methods=["POST"])
def insert_product():
    try:
        request_payload = json.loads(request.form["data"])
        product_id_value = products_dao.insert_new_product(connection, request_payload)

        return jsonify({
            "product_id": product_id_value
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/getAllOrders", methods=["GET"])
def get_all_orders():
    try:
        response = orders_dao.get_all_orders(connection)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/insertOrder", methods=["POST"])
def insert_order():
    try:
        request_payload = json.loads(request.form["data"])
        order_id = orders_dao.insert_order(connection, request_payload)

        return jsonify({
            "order_id": order_id
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/deleteProduct", methods=["POST"])
def delete_product():
    try:
        result = products_dao.delete_product(
            connection,
            request.form["product_id"]
        )

        return jsonify(result)

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    print("=" * 60)
    print("Starting Grocery Store Management System Server")
    print("Server URL : http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )