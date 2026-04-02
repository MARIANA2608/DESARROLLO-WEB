from conexion.conexion import get_connection

def listar_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, c.nombre_categoria
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        ORDER BY p.id_producto DESC
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def insertar_producto(nombre, descripcion, precio, stock, id_categoria):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO productos(nombre, descripcion, precio, stock, id_categoria)
        VALUES (%s,%s,%s,%s,%s)
    """, (nombre, descripcion, precio, stock, id_categoria))

    conn.commit()
    cursor.close()
    conn.close()

def obtener_producto_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id,))
    data = cursor.fetchone()

    cursor.close()
    conn.close()
    return data

def actualizar_producto(id, nombre, descripcion, precio, stock, id_categoria):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE productos
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s, id_categoria=%s
        WHERE id_producto=%s
    """, (nombre, descripcion, precio, stock, id_categoria, id))

    conn.commit()
    cursor.close()
    conn.close()

def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()