from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()

    query = """
    SELECT
        products.product_id,
        products.name,
        products.uom_id,
        products.price_per_unit,
        uom.uom_name
    FROM products
    INNER JOIN uom
        ON products.uom_id = uom.uom_id
    """

    cursor.execute(query)

    response = []

    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            "product_id": product_id,
            "name": name,
            "uom_id": uom_id,
            "price_per_unit": price_per_unit,
            "uom_name": uom_name
        })

    cursor.close()
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit)"
             "VALUES (%s, %s, %s)")
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])

    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()

    # Check if product exists in order_details
    cursor.execute(
        "SELECT COUNT(*) FROM order_details WHERE product_id=%s",
        (product_id,)
    )

    count = cursor.fetchone()[0]

    if count > 0:
        return {
            "success": False,
            "message": "This product has already been used in an order and cannot be deleted."
        }

    cursor.execute(
        "DELETE FROM products WHERE product_id=%s",
        (product_id,)
    )

    connection.commit()

    return {
        "success": True,
        "message": "Product deleted successfully."
    }

if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_all_products(connection))
    print(insert_new_product(connection, {
        'product_name': 'potatoes',
        'uom_id': '1',
        'price_per_unit': 10
    }))