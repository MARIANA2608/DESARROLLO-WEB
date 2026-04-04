from conexion.conexion import get_connection


def listar_clientes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes ORDER BY id_cliente DESC")
    clientes = cursor.fetchall()

    cursor.close()
    conn.close()
    return clientes


def insertar_cliente(nombres, cedula, telefono, direccion):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes (nombres, cedula, telefono, direccion)
        VALUES (%s, %s, %s, %s)
    """, (nombres, cedula, telefono, direccion))

    conn.commit()
    cursor.close()
    conn.close()


def obtener_cliente_por_id(id_cliente):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s", (id_cliente,))
    cliente = cursor.fetchone()

    cursor.close()
    conn.close()
    return cliente


def actualizar_cliente(id_cliente, nombres, cedula, telefono, direccion):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET nombres=%s, cedula=%s, telefono=%s, direccion=%s
        WHERE id_cliente=%s
    """, (nombres, cedula, telefono, direccion, id_cliente))

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_cliente(id_cliente):
    """
    Retorna True si se eliminó.
    Retorna False si no se puede eliminar porque tiene pedidos asociados.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si el cliente tiene pedidos asociados
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE id_cliente=%s", (id_cliente,))
    resultado = cursor.fetchone()

    if resultado[0] > 0:
        cursor.close()
        conn.close()
        return False

    cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id_cliente,))
    conn.commit()

    cursor.close()
    conn.close()
    return True