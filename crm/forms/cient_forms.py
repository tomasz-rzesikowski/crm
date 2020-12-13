from flask_wtf import FlaskForm
from regex import regex
from wtforms import StringField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError

from ..models import Client


def proper_regexp(regexp='', message=''):
    def _proper_regexp(form, field):
        if regex.fullmatch(regexp, field.data) is None:
            raise ValidationError(message)

    return _proper_regexp


class ClientForm(FlaskForm):
    def __init__(self, button_label, **kwargs):
        super(ClientForm, self).__init__(**kwargs)
        self.button.label.text = button_label

    name = StringField(
        'Imię',
        validators=[
            proper_regexp(
                regexp=r'(\p{Lu}\p{Ll}+){1,2}',
                message='Dozwolone tylko imiona zaczynające się dużą literą i skłądające się z samych liter'
            )
        ]
    )

    surname = StringField(
        'Nazwisko',
        validators=[
            proper_regexp(
                regexp=r'((\p{Lu}\p{Ll}+)([- ]?)(\p{Lu}\p{Ll}+)?)?',
                message='Dozwolone tylko nazwiska zaczynające się dużą literą i skłądające się z samych liter'
            )
        ]
    )

    company = StringField(
        'Firma'
    )

    address_street_and_number = StringField(
        'Adres',
        description='Ulica i nr'
    )

    address_zipcode_and_city = StringField(
        'Miejscowość',
        description='Kod pocztowy i miejscowość'
    )

    phone = StringField(
        'Numer tel.',
        validators=[
            proper_regexp(
                regexp='([+]?[0-9 ]{9,16})?',
                message='Dozwolone tylko znak plus, liczby i spacje'
            )
        ]
    )

    email = StringField(
        'Email',
        validators=[
            Email(
                message='Wprowadż poprawny adres email'
            )
        ]
    )

    button = SubmitField()

    def validate_unique_constrain(self, base_idx=None):
        client = Client.get_by_unique_constrain(name=self.name.data,
                                                surname=self.surname.data,
                                                phone=self.phone.data,
                                                email=self.email.data)
        if base_idx:
            if client.id != base_idx:
                raise ValidationError(f'Istnieje klient {self.name.data} {self.surname.data}'
                                      f' z numerem tel {self.phone.data} i emailem {self.email.data}')

        if client:
            raise ValidationError(f'Istnieje klient {self.name.data} {self.surname.data}'
                                  f' z numerem tel {self.phone.data} i emailem {self.email.data}')

        return True

    def validate_model(self):
        if self.surname.data is None and self.phone.data is None and self.email.data is None:
            raise ValidationError('Musisz podać nazwisko, numer tel lub email')

        return True
