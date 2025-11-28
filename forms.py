from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, Optional, NumberRange

class LoginForm(FlaskForm):
    nombre = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class ProductoFiltroForm(FlaskForm):
    id = IntegerField('ID', validators=[Optional()])
    nombre = StringField('Nombre', validators=[Optional()])
    precio_min = DecimalField('Precio mínimo', validators=[Optional()])
    precio_max = DecimalField('Precio máximo', validators=[Optional()])
    cantidad_min = IntegerField('Cantidad mínima', validators=[Optional(), NumberRange(min=0)])
    cantidad_max = IntegerField('Cantidad máxima', validators=[Optional(), NumberRange(min=0)])
    departamento = StringField('Departamento', validators=[Optional()])
    almacen = SelectField('Almacén', validators=[Optional()], coerce=int)
    usuario_modificacion = StringField('Usuario que modificó', validators=[Optional()])
    filtro_modificaciones = SelectField(
        'Mostrar',
        choices=[('todos', 'Todos'), ('ultimos', 'Últimos modificados')],
        default='todos'
    )
    submit = SubmitField('Filtrar')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    departamento = StringField('Departamento', validators=[DataRequired()])
    almacen = SelectField('Almacén', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

class AlmacenFiltroForm(FlaskForm):
    id = IntegerField('ID', validators=[Optional()])
    nombre = StringField('Nombre', validators=[Optional()])
    usuario_modificacion = StringField('Usuario que modificó', validators=[Optional()])
    filtro_modificaciones = SelectField(
        'Mostrar',
        choices=[('todos', 'Todos'), ('ultimos', 'Últimos modificados')],
        default='todos'
    )
    submit = SubmitField('Filtrar')

class AlmacenForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Guardar')
