import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="54321",
            database="restaurante_db"
        )
        return conn
    except Error as e:
        print("Error al conectar a MariaDB:", e)
        return None