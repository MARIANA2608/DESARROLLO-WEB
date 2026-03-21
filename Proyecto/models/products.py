# clase producto 
class Producto:
    def __init__(self, id_producto=None, nombre='', descripcion='', precio=0, stock=0):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

# Lista de productos 