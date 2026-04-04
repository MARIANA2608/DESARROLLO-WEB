from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class DetallePedidoForm(FlaskForm):
    id_producto = SelectField("Producto", coerce=int, validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Agregar al Pedido")