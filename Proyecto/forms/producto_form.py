from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class ProductoForm(FlaskForm):
    nombre = StringField("Nombre del Producto", validators=[DataRequired(), Length(min=2, max=150)])
    descripcion = TextAreaField("Descripción", validators=[Length(max=255)])
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    id_categoria = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Guardar")