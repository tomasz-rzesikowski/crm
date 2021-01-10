from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired

from ..utils import proper_regexp


class LoginForm(FlaskForm):
    initials = StringField('Inicjały', validators=[
        InputRequired(message='Pole jest wymagane.'),
        DataRequired(message='Pole jest wymagane.'),
        proper_regexp(
            regexp=r'(\p{Lu}){1,5}',
            message='Dozwolone tylko duże litery. Maksymalnie pięć')
    ])
    password = PasswordField('Hasło', validators=[DataRequired(message='Pole jest wymagane.')])
    remember_me = BooleanField('Pozostaw mnie zalogowanym')
    submit = SubmitField('Zaloguj się')
