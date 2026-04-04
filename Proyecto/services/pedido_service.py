from conexion.conexion import get_connection


def listar_pedidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.id_pedido, p.fecha, p.total,
               c.nombres
        FROM pedidos p
        INNER JOIN clientes c ON p.id_cliente = c.id_cliente
        ORDER BY p.id_pedido DESC
    """)

    pedidos = cursor.fetchall()

    cursor.close()
    conn.close()
    return pedidos


def insertar_pedido(id_cliente):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pedidos (id_cliente, total)
        VALUES (%s, 0)
    """, (id_cliente,))

    conn.commit()
    pedido_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return pedido_id


def obtener_pedido_por_id(id_pedido):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.id_pedido, p.fecha, p.total,
               c.nombres, c.cedula, c.telefono, c.direccion
        FROM pedidos p
        INNER JOIN clientes c ON p.id_cliente = c.id_cliente
        WHERE p.id_pedido = %s
    """, (id_pedido,))

    pedido = cursor.fetchone()

    cursor.close()
    conn.close()
    return pedido


def actualizar_total_pedido(id_pedido):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT SUM(subtotal) AS total
        FROM detalle_pedido
        WHERE id_pedido = %s
    """, (id_pedido,))

    resultado = cursor.fetchone()
    total = resultado["total"]

    if total is None:
        total = 0

    cursor.close()

    cursor2 = conn.cursor()
    cursor2.execute("UPDATE pedidos SET total=%s WHERE id_pedido=%s", (total, id_pedido))

    conn.commit()
    cursor2.close()
    conn.close()


def eliminar_pedido(id_pedido):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM detalle_pedido WHERE id_pedido=%s", (id_pedido,))
    cursor.execute("DELETE FROM pedidos WHERE id_pedido=%s", (id_pedido,))

    conn.commit()
    cursor.close()
    conn.close()
    return True