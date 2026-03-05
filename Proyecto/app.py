from flask import Flask, render_template, url_for, request, redirect, flash
from form import ProductoForm
from inventario.bd import init_db, get_db_connection
from inventario.inventario import Inventario
from inventario.productos import Producto

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'
init_db()
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



    




if __name__ == '__main__':
    app.run(debug=True)
