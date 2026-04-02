from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class PedidoForm(FlaskForm):
    id_cliente = SelectField("Cliente", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Guardar Pedido")