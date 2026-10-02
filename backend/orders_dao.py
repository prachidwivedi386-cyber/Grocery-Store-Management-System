from datetime import datetime
from sql_connection import get_sql_connection


def insert_order(connection, order):
    cursor = connection.cursor()

    try:
        # Insert into orders table
        order_query = """
        INSERT INTO orders (customer_name, total, datetime)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(
            order_query,
            (
                order["customer_name"],
                float(order["total"]),
                datetime.now()
            )
        )

        order_id = cursor.lastrowid

        # Insert order details
        order_details_query = """
        INSERT INTO order_details
        (order_id, product_id, quantity, total_price)
        VALUES (%s, %s, %s, %s)
        """

        order_details_data = []

        for item in order["order_details"]:

            # Check product exists
            cursor.execute(
                "SELECT product_id FROM products WHERE product_id=%s",
                (item["product_id"],)
            )

            product = cursor.fetchone()

            if not product:
                raise Exception(
                    f"Product ID {item['product_id']} does not exist."
                )

            order_details_data.append(
                (
                    order_id,
                    int(item["product_id"]),
                    int(item["quantity"]),
                    float(item["total_price"])
                )
            )

        cursor.executemany(
            order_details_query,
            order_details_data
        )

        connection.commit()

        return order_id

    except Exception as e:

        connection.rollback()

        print("Insert Error:", e)

        return None

    finally:

        cursor.close()


def get_order_details(connection, order_id):

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        od.order_id,
        od.product_id,
        p.name AS product_name,
        od.quantity,
        od.total_price,
        p.price_per_unit
    FROM order_details od
    JOIN products p
    ON od.product_id = p.product_id
    WHERE od.order_id=%s
    """

    cursor.execute(query, (order_id,))

    response = cursor.fetchall()

    cursor.close()

    return response


def get_all_orders(connection):

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        order_id,
        customer_name,
        total,
        datetime
    FROM orders
    ORDER BY order_id DESC
    """

    cursor.execute(query)

    response = cursor.fetchall()

    cursor.close()

    for order in response:
        order["order_details"] = get_order_details(
            connection,
            order["order_id"]
        )

    return response


if __name__ == "__main__":

    connection = get_sql_connection()

    print("Opening MySQL connection...")

    test_order = {
        "customer_name": "Prachi",
        "total": 210,
        "order_details": [
            {
                "product_id": 1,
                "quantity": 2,
                "total_price": 180
            },
            {
                "product_id": 2,
                "quantity": 1,
                "total_price": 30
            }
        ]
    }

    order_id = insert_order(connection, test_order)

    if order_id:
        print("Order inserted successfully.")
        print("Order ID:", order_id)
        print(get_order_details(connection, order_id))
    else:
        print("Order insert failed.")

    print(get_all_orders(connection))

    connection.close()