from conexion.conexion import get_connection

def listar_detalle(id_pedido):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT d.id_detalle, d.cantidad, d.subtotal,
               p.nombre, p.precio
        FROM detalle_pedido d
        INNER JOIN productos p ON d.id_producto = p.id_producto
        WHERE d.id_pedido=%s
    """, (id_pedido,))

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def agregar_producto_a_pedido(id_pedido, id_producto, cantidad):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT precio FROM productos WHERE id_producto=%s", (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        return False

    precio = float(producto["precio"])
    subtotal = precio * int(cantidad)

    cursor2 = conn.cursor()
    cursor2.execute("""
        INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad, subtotal)
        VALUES (%s,%s,%s,%s)
    """, (id_pedido, id_producto, cantidad, subtotal))

    conn.commit()
    cursor.close()
    cursor2.close()
    conn.close()
    return True

def eliminar_detalle(id_detalle):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM detalle_pedido WHERE id_detalle=%s", (id_detalle,))
    conn.commit()
    cursor.close()
    conn.close()