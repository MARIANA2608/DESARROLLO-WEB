from conexion.conexion import get_connection

def listar_pedidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos ORDER BY id_pedido DESC")
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return pedidos

def insertar_pedido(id_cliente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos(id_cliente, total) VALUES (%s, 0)", (id_cliente,))
    conn.commit()
    pedido_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return pedido_id

def obtener_pedido_por_id(id_pedido):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos WHERE id_pedido=%s", (id_pedido,))
    pedido = cursor.fetchone()
    cursor.close()
    conn.close()
    return pedido

def eliminar_pedido(id_pedido):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id_pedido=%s", (id_pedido,))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_total_pedido(id_pedido):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedidos p
        SET total = (SELECT SUM(subtotal) FROM detalle_pedido WHERE id_pedido=p.id_pedido)
        WHERE p.id_pedido=%s
    """, (id_pedido,))
    conn.commit()
    cursor.close()
    conn.close()