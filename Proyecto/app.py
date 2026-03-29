from flask import Flask, render_template, url_for, request, redirect, flash
from form import ProductoForm
from inventario.bd import init_db, get_db_connection
from inventario.inventario import Inventario
from inventario.productos import Producto
from flask_sqlalchemy import SQLAlchemy
from inventario.inventario_persistencia import guardar_csv, leer_csv, guardar_json, leer_json,  guardar_txt, leer_txt
from inventario.models import db, ProductoORM
from conexion.conexion import get_connection
from services.producto_service import *
from forms.producto_form import ProductoForm

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms.login_form import LoginForm
from forms.registro_form import RegistroForm
from services.usuario_service import *

from fpdf import FPDF
from flask import make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secretaa'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión para acceder a esta página'
login_manager.login_message_category = 'warning'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invent.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
"""
db.init_app(app)

with app.app_context():
    db.create_all()

inventario = Inventario()
inventario.cargar_desde_db()
"""
@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        password = form.password.data

        usuario_existente = obtener_usuario_por_email(email)
        if usuario_existente:
            flash('Ya existe un usuario con ese correo', 'danger')
            return redirect(url_for('registro'))

        password_hash = generate_password_hash(password)

        registrar_usuario(nombre, email, password_hash)

        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('login'))

    return render_template('auth/registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        usuario = obtener_usuario_por_email(email)

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

# ruta de exportar PDF 
@app.route('/exportar/pdf')
@login_required
def exportar_pdf():
    productos = listar_productos()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Reporte de Productos ", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(20, 10, "ID", 1)
    pdf.cell(60, 10, "Nombre", 1)
    pdf.cell(30, 10, "Precio", 1)
    pdf.cell(30, 10, "Stock", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)

    for p in productos:
        pdf.cell(20, 10, str(p['id_producto']), 1)
        pdf.cell(60, 10, p['nombre'], 1)
        pdf.cell(30, 10, f"${p['precio']}", 1)
        pdf.cell(30, 10, str(p['stock']), 1)
        pdf.ln()

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename='productos.pdf')
    response.headers.set('Content-Type', 'application/pdf')

    return response

@app.route('/')

def inicio():
    return render_template("index.html")

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

@app.route('/contactos')
def contact():
    return render_template("contactos.html")

@app.route('/about')
def about():
    return render_template("about.html")

"""
# ruta de productos sqlite
@app.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        cantidad = form.cantidad.data
        precio = form.precio.data
        inventario.agregar_producto(nombre, descripcion, cantidad, precio)
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('productos_listar'))
    return render_template('producto_form.html', form=form)

# ruta para listar productos con SQLITE
@app.route('/productos')
def productos_listar():
    inventario.cargar_desde_db()  # Asegurarse de cargar los productos más recientes
    productos = list(inventario.productos.values())
    return render_template('productos.html', productos=productos)

# ruta para editar producto con SQLITE
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    producto = inventario.productos.get(id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos_listar'))
    
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        cantidad = form.cantidad.data
        precio = form.precio.data
        inventario.actualizar_producto(id, nombre, descripcion, cantidad, precio)
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('productos_listar'))
    
    return render_template('producto_form.html', form=form, producto=producto)

# ruta para eliminar producto con SQLITE
@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def producto_eliminar(id):
    inventario.eliminar_producto(id)
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('productos_listar'))
"""
#  PARA REALIZAR EL CRUD CON MYSQL 
@app.route('/productos')
@login_required
def productos_listar():

    productos = listar_productos()

    return render_template(
        'productos/listar.html',
        productos=productos
    )


@app.route('/productos/nuevo', methods=['GET','POST'])
def producto_nuevo():
    form = ProductoForm()

    if form.validate_on_submit():
        insertar_producto(
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data
        )
        flash("Producto guardado")
        return redirect(url_for('productos_listar'))

    return render_template('productos/formulario.html', form=form)


@app.route('/productos/eliminar/<int:id>')
def producto_eliminar(id):
    eliminar_producto(id)
    flash("Producto eliminado")
    return redirect(url_for('productos_listar'))

# ruta de productos 
@app.route('/productos/editar/<int:id>', methods=['GET','POST'])
def producto_editar(id):

    producto = obtener_producto_por_id(id)
    form = ProductoForm(data=producto)

    if form.validate_on_submit():
        actualizar_producto(
            id,
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data
        )
        flash("Producto actualizado")
        return redirect(url_for('productos_listar'))

    return render_template('productos/formulario.html', form=form, producto=producto)



# ruta para los datos persistentes
@app.route('/datos', methods=['GET', 'POST'])
def datos():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        cantidad = request.form.get('cantidad', '0').strip()
        precio = request.form.get('precio', '0').strip()

        dic = {
            'nombre': nombre,
            'descripcion': descripcion,
            'cantidad': cantidad,
            'precio': precio
        }

        guardar_txt(f"{nombre}, {descripcion}, {cantidad}, {precio}")
        guardar_json(dic)
        guardar_csv(dic)   

        flash('Datos guardados exitosamente', 'success')
        return redirect(url_for('datos'))

    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()
    return render_template('datos.html', datos_txt=datos_txt, datos_json=datos_json, datos_csv=datos_csv)

# ruta de conexion a mysql
@app.route('/db_test')
def db_test():
    try:
        conn = get_connection()

        if conn is None:
            flash('No se pudo conectar a la base de datos', 'danger')
            
        cursor = conn.cursor()
        cursor.execute('SELECT * from usuario')
        result = cursor.fetchall()
        cursor.close()
        flash(f'Conexión exitosa. Usuarios: {result}', 'success')
        conn.close()
        return str(result)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'danger')
        return f'Error: {e}'
    

if __name__ == '__main__':
    app.run(debug=True)