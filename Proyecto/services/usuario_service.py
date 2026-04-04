from conexion.conexion import get_connection
from models.usuario import Usuario


def registrar_usuario(nombre, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios(nombre, email, password)
        VALUES (%s, %s, %s)
    """, (nombre, email, password_hash))

    conn.commit()
    cursor.close()
    conn.close()


def obtener_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return Usuario(
            usuario["id_usuario"],
            usuario["nombre"],
            usuario["email"],
            usuario["password"]
        )
    return None


def obtener_usuario_por_id(id_usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (int(id_usuario),))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return Usuario(
            usuario["id_usuario"],
            usuario["nombre"],
            usuario["email"],
            usuario["password"]
        )
    return None