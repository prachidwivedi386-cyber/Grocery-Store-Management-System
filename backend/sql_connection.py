import mysql.connector
from mysql.connector import Error

__cnx = None

def get_sql_connection():
    global __cnx

    try:
        if __cnx is None or not __cnx.is_connected():
            print("Opening MySQL connection...")

            __cnx = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",      # Replace with your MySQL password
                database="gs"
            )

        return __cnx

    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None