from flask_wtf import FlaskForm
from regex import regex
from wtforms import StringField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError

from ..models import User


def proper_regexp(regexp='', message=''):
    def _proper_regexp(form, field):
        if regex.fullmatch(regexp, field.data) is None:
            raise ValidationError(message)

    return _proper_regexp


class UserForm(FlaskForm):
    def __init__(self, button_label, base_idx=None, **kwargs):
        super(UserForm, self).__init__(**kwargs)
        self.button.label.text = button_label
        self.base_idx = base_idx

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

    def validate_initials(self, initials_field):
        if self.base_idx and User.get_by_initials(initials_field.data).id != self.base_idx:
            raise ValidationError('Istnieje użytkownik z takimi inicjałami')

        if self.base_idx is None and User.get_by_initials(initials_field.data):
            raise ValidationError('Istnieje użytkownik z takimi inicjałami')


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

    def validate_email(self, email_field):
        if self.base_idx and User.get_by_email(email_field.data).id != self.base_idx:
            raise ValidationError('Istnieje użytkownik z takim emailem')

        if self.base_idx is None and User.get_by_email(email_field.data):
            raise ValidationError('Istnieje użytkownik z takim emailem')

    button = SubmitField()

    @staticmethod
    def validate_model(user):
        if User.query.get(user.initials).first():
            raise ValidationError('Istnieje użytkownik z takimi inicjałami')
