from flask_wtf import FlaskForm
from regex import regex
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError

from ..models import Offer


def proper_regexp(regexp='', message=''):
    def _proper_regexp(form, field):
        if regex.fullmatch(regexp, str(field.data)) is None:
            raise ValidationError(message)

    return _proper_regexp


class OfferForm(FlaskForm):
    def __init__(self, button_label, base_idx=None, **kwargs):
        super(OfferForm, self).__init__(**kwargs)
        self.button.label.text = button_label
        self.base_idx = base_idx

    form_fields = ['year', 'offer_number', 'button']

    year = IntegerField('Rok',
                        validators=[DataRequired(),
                                    proper_regexp(regexp=r'\d{4}', message='Podaj poprawny rok')
                                    ])

    offer_number = IntegerField('Numer oferty',
                                validators=[DataRequired(),
                                            proper_regexp(regexp=r'\d{1,}', message='Tylko cyfry')
                                            ])

    offer_version = StringField("Wersja oferty",
                                validators=[DataRequired(),
                                            proper_regexp(regexp=r'\p{Lu}', message='Jedna duża litera')
                                            ])

    button = SubmitField()

    def validate_unique_constrain(self, base_idx=None):
        client = Offer.get_by_unique_constrain(year=self.year.data,
                                               offer_number=self.offer_number.data,
                                               offer_version=self.offer_version.data)
        if base_idx:
            if client.id != base_idx:
                raise ValidationError(f'Istnieje oferta {self.year.data} {self.offer_number.data}{self.offer_version.data}')

        if client:
            raise ValidationError(f'Istnieje oferta {self.year.data} {self.offer_number.data}{self.offer_version.data}')

        return True
