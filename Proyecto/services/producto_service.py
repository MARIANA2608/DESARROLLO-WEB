from conexion.conexion import get_connection


def listar_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock,
               p.id_categoria, c.nombre_categoria
        FROM productos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        ORDER BY p.id_producto DESC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()
    return productos


def insertar_producto(nombre, descripcion, precio, stock, id_categoria):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO productos(nombre, descripcion, precio, stock, id_categoria)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, descripcion, precio, stock, id_categoria))

    conn.commit()
    cursor.close()
    conn.close()


def obtener_producto_por_id(id_producto):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id_producto,))
    producto = cursor.fetchone()

    cursor.close()
    conn.close()
    return producto


def actualizar_producto(id_producto, nombre, descripcion, precio, stock, id_categoria):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE productos
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s, id_categoria=%s
        WHERE id_producto=%s
    """, (nombre, descripcion, precio, stock, id_categoria, id_producto))

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_producto(id_producto):
    """
    Retorna False si el producto ya está en pedidos (detalle_pedido).
    Retorna True si se elimina correctamente.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si el producto está asociado a pedidos
    cursor.execute("SELECT COUNT(*) FROM detalle_pedido WHERE id_producto=%s", (id_producto,))
    resultado = cursor.fetchone()

    if resultado[0] > 0:
        cursor.close()
        conn.close()
        return False

    cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
    conn.commit()

    cursor.close()
    conn.close()
    return True