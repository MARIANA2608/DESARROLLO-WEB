from conexion.conexion import get_connection

def listar_categorias():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def insertar_categoria(nombre_categoria):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categorias(nombre_categoria) VALUES (%s)", (nombre_categoria,))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_categoria_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias WHERE id_categoria=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

def actualizar_categoria(id, nombre_categoria):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE categorias SET nombre_categoria=%s WHERE id_categoria=%s", (nombre_categoria, id))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_categoria(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE id_categoria=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()