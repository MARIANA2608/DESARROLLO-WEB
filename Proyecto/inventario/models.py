from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProductoORM(db.Model):
    __tablename__ = 'productos_orm'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<ProductoORM {self.nombre}>'