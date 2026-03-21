from conexion.conexion import get_connection

def listar_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM producto")

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return productos


def insertar_producto(nombre, descripcion, precio, stock):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO producto(nombre, descripcion, precio, stock)
        VALUES (%s,%s,%s,%s)
    """, (nombre, descripcion, precio, stock))

    conn.commit()

    cursor.close()
    conn.close()


def eliminar_producto(id_producto):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM producto WHERE id_producto=%s", (id_producto,))

    conn.commit()

    cursor.close()
    conn.close()


def actualizar_producto(id_producto, nombre, descripcion, precio, stock):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE producto
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s
        WHERE id_producto=%s
    """, (nombre, descripcion, precio, stock, id_producto))

    conn.commit()

    cursor.close()
    conn.close()

def obtener_producto_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM producto WHERE id_producto= %s", (id,))
    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    return producto
