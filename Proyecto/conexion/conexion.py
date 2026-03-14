# conexion a mysql
import mysql.connector
from mysql.connector import Error
def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Sistema_factura',
            user='root',
            password='root'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
    