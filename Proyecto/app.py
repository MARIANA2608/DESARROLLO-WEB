from flask import Flask, render_template, url_for, request, redirect, flash
from form import ProductoForm
from inventario.bd import init_db, get_db_connection
from inventario.inventario import Inventario
from inventario.productos import Producto
from flask_sqlalchemy import SQLAlchemy
from inventario.inventario_persistencia import guardar_csv, leer_csv, guardar_json, leer_json,  guardar_txt, leer_txt
from inventario.models import db, ProductoORM
from conexion.conexion import get_connection
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

db.init_app(app)

with app.app_context():
    db.create_all()

inventario = Inventario()
inventario.cargar_desde_db()

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

# ruta de productos
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

# ruta para listar productos
@app.route('/productos')
def productos_listar():
    inventario.cargar_desde_db()  # Asegurarse de cargar los productos más recientes
    productos = list(inventario.productos.values())
    return render_template('productos.html', productos=productos)

# ruta para editar producto
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

# ruta para eliminar producto
@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def producto_eliminar(id):
    inventario.eliminar_producto(id)
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('productos_listar'))

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
