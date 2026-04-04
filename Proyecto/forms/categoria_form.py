from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CategoriaForm(FlaskForm):
    nombre_categoria = StringField("Nombre de la Categoría", validators=[DataRequired()])
    submit = SubmitField("Guardar")