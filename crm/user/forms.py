from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo, InputRequired

from .models import User
from ..utils import proper_regexp


class UserForm(FlaskForm):
    name = StringField('Imię', validators=[
            InputRequired(message='Pole jest wymagane.'),
            DataRequired(message='Pole jest wymagane.'),
            proper_regexp(
                regexp=r'(\p{Lu}\p{Ll}+){1,2}',
                message='Dozwolone tylko imiona zaczynające się dużą literą i skłądające się z samych liter')
    ])

    surname = StringField('Nazwisko', validators=[
            InputRequired(message='Pole jest wymagane.'),
            DataRequired(message='Pole jest wymagane.'),
            proper_regexp(
                regexp=r'(\p{Lu}\p{Ll}+)([- ]?)(\p{Lu}\p{Ll}+)?',
                message='Dozwolone tylko nazwiska zaczynające się dużą literą i skłądające się z samych liter')
    ])

    initials = StringField('Inicjały', validators=[
            InputRequired(message='Pole jest wymagane.'),
            DataRequired(message='Pole jest wymagane.'),
            proper_regexp(
                regexp=r'(\p{Lu}){1,5}',
                message='Dozwolone tylko duże litery. Maksymalnie pięć')
    ])

    phone = StringField('Numer tel.', validators=[
            InputRequired(message='Pole jest wymagane.'),
            DataRequired(message='Pole jest wymagane.'),
            proper_regexp(
                regexp='[+]?[0-9 ]{9,16}',
                message='Dozwolone tylko znak plus, liczby i spacje')
    ])

    email = StringField('Email', validators=[
            InputRequired(message='Pole jest wymagane.'),
            DataRequired(message='Pole jest wymagane.'),
            Email(message='Wprowadż poprawny adres email.')
    ])

    submit = SubmitField()

    def validate_on_submit(self):
        rv = FlaskForm.validate_on_submit(self)
        if not rv:
            return False

        user = User.get_by_initials(self.initials.data)

        if user is not None:
            if not hasattr(self, 'id'):
                self.initials.errors.append(
                    f'Istnieje użytkownik z inicjałami {self.initials.data}.')
                return False

            if hasattr(self, 'id') and user.id != self.id.data:
                self.initials.errors.append(
                    f'Istnieje użytkownik z inicjałami {self.initials.data}.')
                return False

        user = User.get_by_email(self.email.data)
        if user is not None:
            if not hasattr(self, 'id'):
                self.email.errors.append(
                    f'Istnieje użytkownik z emailem {self.email.data}.')
                return False

            if hasattr(self, 'id') and user.id != self.id.data:
                self.email.errors.append(
                    f'Istnieje użytkownik z emailem {self.email.data}.')
                return False

        return True


class NewUserForm(UserForm):
    submit = SubmitField('Stwórz użytkownika')
    password = PasswordField('Hasło', validators=[
        DataRequired(message='Pole jest wymagane.'),
        EqualTo('password2', message='Hasła muszą się zgadzać.')
    ])
    password2 = PasswordField('Powtórz hasło', validators=[DataRequired(message='Pole jest wymagane.')])


class EditUserForm(UserForm):
    id = HiddenField()
    submit = SubmitField('Zapisz')


class DeleteUserForm(FlaskForm):
    submit = SubmitField('Usuń')

