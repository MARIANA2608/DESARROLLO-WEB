class Pedido:
    def __init__(self, id_pedido=None, id_cliente=None, fecha=None, total=0):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.fecha = fecha
        self.total = total