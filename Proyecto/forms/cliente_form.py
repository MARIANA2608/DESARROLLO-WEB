from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ClienteForm(FlaskForm):
    nombres = StringField("Nombres", validators=[DataRequired(), Length(min=3, max=120)])
    cedula = StringField("Cédula", validators=[DataRequired(), Length(min=10, max=15)])
    telefono = StringField("Teléfono", validators=[Length(max=20)])
    direccion = StringField("Dirección", validators=[Length(max=200)])
    submit = SubmitField("Guardar")