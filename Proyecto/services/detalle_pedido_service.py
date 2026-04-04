from conexion.conexion import get_connection


def listar_detalle(id_pedido):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT d.id_detalle, d.id_pedido, d.id_producto,
               p.nombre, p.precio,
               d.cantidad, d.subtotal
        FROM detalle_pedido d
        INNER JOIN productos p ON d.id_producto = p.id_producto
        WHERE d.id_pedido = %s
        ORDER BY d.id_detalle DESC
    """, (id_pedido,))

    detalle = cursor.fetchall()

    cursor.close()
    conn.close()
    return detalle


def agregar_producto_a_pedido(id_pedido, id_producto, cantidad):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verificar producto existente y stock disponible
    cursor.execute("SELECT precio, stock, nombre FROM productos WHERE id_producto=%s", (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        return False, "Producto no encontrado."

    stock_disponible = int(producto["stock"])
    cantidad = int(cantidad)

    if cantidad <= 0:
        cursor.close()
        conn.close()
        return False, "La cantidad debe ser mayor a 0."

    if cantidad > stock_disponible:
        cursor.close()
        conn.close()
        return False, f"No hay stock suficiente. Stock disponible: {stock_disponible}"

    precio = float(producto["precio"])
    subtotal = precio * cantidad

    # Insertar detalle
    cursor2 = conn.cursor()
    cursor2.execute("""
        INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, subtotal)
        VALUES (%s, %s, %s, %s)
    """, (id_pedido, id_producto, cantidad, subtotal))

    # Actualizar stock
    cursor2.execute("""
        UPDATE productos
        SET stock = stock - %s
        WHERE id_producto = %s
    """, (cantidad, id_producto))

    conn.commit()

    cursor.close()
    cursor2.close()
    conn.close()

    return True, f"Producto agregado correctamente: {producto['nombre']}"


def eliminar_detalle(id_detalle):
    """
    Elimina el detalle y devuelve el stock al producto.
    Retorna True si elimina.
    Retorna False si no existe.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar detalle
    cursor.execute("SELECT id_producto, cantidad FROM detalle_pedido WHERE id_detalle=%s", (id_detalle,))
    detalle = cursor.fetchone()

    if not detalle:
        cursor.close()
        conn.close()
        return False

    id_producto = detalle["id_producto"]
    cantidad = detalle["cantidad"]

    cursor2 = conn.cursor()

    # Devolver stock
    cursor2.execute("""
        UPDATE productos
        SET stock = stock + %s
        WHERE id_producto = %s
    """, (cantidad, id_producto))

    # Eliminar detalle
    cursor2.execute("DELETE FROM detalle_pedido WHERE id_detalle=%s", (id_detalle,))

    conn.commit()

    cursor.close()
    cursor2.close()
    conn.close()

    return True