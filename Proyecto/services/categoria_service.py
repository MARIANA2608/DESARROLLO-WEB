from conexion.conexion import get_connection


def listar_categorias():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categorias ORDER BY id_categoria DESC")
    categorias = cursor.fetchall()

    cursor.close()
    conexion.close()
    return categorias


def insertar_categoria(nombre_categoria):
    conexion = get_connection()
    cursor = conexion.cursor()

    sql = "INSERT INTO categorias (nombre_categoria) VALUES (%s)"
    cursor.execute(sql, (nombre_categoria,))
    conexion.commit()

    cursor.close()
    conexion.close()


def obtener_categoria_por_id(id_categoria):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categorias WHERE id_categoria = %s", (id_categoria,))
    categoria = cursor.fetchone()

    cursor.close()
    conexion.close()
    return categoria


def actualizar_categoria(id_categoria, nombre_categoria):
    conexion = get_connection()
    cursor = conexion.cursor()

    sql = "UPDATE categorias SET nombre_categoria = %s WHERE id_categoria = %s"
    cursor.execute(sql, (nombre_categoria, id_categoria))
    conexion.commit()

    cursor.close()
    conexion.close()


def eliminar_categoria(id_categoria):
    conexion = get_connection()
    cursor = conexion.cursor()

    # Verificar si hay productos asociados a la categoría
    cursor.execute("SELECT COUNT(*) AS total FROM productos WHERE id_categoria = %s", (id_categoria,))
    resultado = cursor.fetchone()

    if resultado[0] > 0:
        cursor.close()
        conexion.close()
        return False  # No se puede eliminar

    cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,))
    conexion.commit()

    cursor.close()
    conexion.close()
    return True