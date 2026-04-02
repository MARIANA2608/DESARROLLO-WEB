from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    descripcion = StringField("Descripción", validators=[DataRequired()])
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)], places=2)
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])

    id_categoria = SelectField("Categoría", coerce=int, validators=[DataRequired()])

    submit = SubmitField("Guardar")