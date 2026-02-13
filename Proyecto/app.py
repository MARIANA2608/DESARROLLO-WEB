from flask import Flask

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return """
    <h1>Sistema de Gestión de Inventario – TechStore</h1>
    <p>Bienvenido al sistema de administración de productos.</p>
    <ul>
        <li>Consultar producto: /item/A123</li>
        <li>Consultar categoría: /categoria/electronica</li>
        <li>Ver stock por cantidad: /stock/10</li>
    </ul>
    """

# Ruta dinámica para consultar producto por código
@app.route('/item/<codigo>')
def item(codigo):
    return f"""
    <h2>Consulta de Producto</h2>
    <p>Código del producto: {codigo}</p>
    <p>Estado: Disponible en inventario.</p>
    <a href="/">Volver al inicio</a>
    """

# Ruta dinámica para categoría
@app.route('/categoria/<nombre>')
def categoria(nombre):
    return f"""
    <h2>Categoría seleccionada</h2>
    <p>Mostrando productos de la categoría: {nombre}</p>
    <a href="/">Volver al inicio</a>
    """

# Ruta dinámica que solo acepta números
@app.route('/stock/<int:cantidad>')
def stock(cantidad):
    return f"""
    <h2>Consulta de Stock</h2>
    <p>Productos con al menos {cantidad} unidades disponibles.</p>
    <a href="/">Volver al inicio</a>
    """

if __name__ == '__main__':
    app.run()
