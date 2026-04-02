class Producto:
    def __init__(self, id_producto=None, nombre="", descripcion="", precio=0, stock=0, id_categoria=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria