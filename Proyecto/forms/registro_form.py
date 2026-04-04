from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegistroForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Registrarse")