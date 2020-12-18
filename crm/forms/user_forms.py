from flask_wtf import FlaskForm
from regex import regex
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import Email, DataRequired, ValidationError

from ..models import User


def proper_regexp(regexp='', message=''):
    def _proper_regexp(form, field):
        if regex.fullmatch(regexp, field.data) is None:
            raise ValidationError(message)

    return _proper_regexp


class UserForm(FlaskForm):
    name = StringField(
        'Imię',
        validators=[
            DataRequired(),
            proper_regexp(
                regexp=r'(\p{Lu}\p{Ll}+){1,2}',
                message='Dozwolone tylko imiona zaczynające się dużą literą i skłądające się z samych liter'
            )
        ]
    )

    surname = StringField(
        'Nazwisko',
        validators=[
            DataRequired(),
            proper_regexp(
                regexp=r'(\p{Lu}\p{Ll}+)([- ]?)(\p{Lu}\p{Ll}+)?',
                message='Dozwolone tylko nazwiska zaczynające się dużą literą i skłądające się z samych liter'
            )
        ]
    )

    initials = StringField(
        'Inicjały',
        validators=[
            DataRequired(),
            proper_regexp(
                regexp=r'(\p{Lu}){1,5}',
                message='Dozwolone tylko duże litery. Maksymalnie pięć'
            )
        ]
    )

    phone = StringField(
        'Numer tel.',
        validators=[
            DataRequired(),
            proper_regexp(
                regexp='[+]?[0-9 ]{9,16}',
                message='Dozwolone tylko znak plus, liczby i spacje'
            )
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired('Pole nie może być puste.'),
            Email(
                message='Wprowadż poprawny adres email'
            )
        ]
    )

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


class EditUserForm(UserForm):
    id = HiddenField()
    submit = SubmitField('Zapisz')


class DeleteUserForm(FlaskForm):
    submit = SubmitField('Usuń')
