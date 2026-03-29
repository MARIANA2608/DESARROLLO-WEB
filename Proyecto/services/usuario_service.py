from conexion.conexion import get_connection
from models.usuario import Usuario

def registrar_usuario(nombre, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, password)
        VALUES (%s, %s, %s)
    """, (nombre, email, password))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if data:
        return Usuario(
            data['id_usuario'],
            data['nombre'],
            data['email'],
            data['password']
        )
    return None

def obtener_usuario_por_id(id_usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if data:
        return Usuario(
            data['id_usuario'],
            data['nombre'],
            data['email'],
            data['password']
        )
    return None