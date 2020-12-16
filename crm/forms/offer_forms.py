from flask_wtf import FlaskForm
from regex import regex
from wtforms import IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, ValidationError

from ..models import Offer


def proper_regexp(regexp='', message=''):
    def _proper_regexp(form, field):
        if regex.fullmatch(regexp, str(field.data)) is None:
            raise ValidationError(message)

    return _proper_regexp


class OfferForm(FlaskForm):
    year = IntegerField('Rok',
                        validators=[DataRequired(),
                                    proper_regexp(regexp=r'\d{4}', message='Podaj poprawny rok.')
                                    ])

    offer_number = IntegerField('Numer oferty',
                                validators=[DataRequired(),
                                            proper_regexp(regexp=r'\d{1,}', message='Tylko cyfry.')
                                            ])

    offer_version = StringField("Wersja oferty",
                                validators=[DataRequired(),
                                            proper_regexp(regexp=r'\p{Lu}', message='Jedna duża litera.')
                                            ])

    submit = SubmitField()

    def validate_on_submit(self):
        rv = FlaskForm.validate_on_submit(self)
        if not rv:
            return False

        offer = Offer.get_by_unique_constrain(year=self.year.data,
                                              offer_number=self.offer_number.data,
                                              offer_version=self.offer_version.data)
        if offer is not None:
            if not hasattr(self, 'id'):
                self.submit.errors.append(
                    f'Istnieje już oferta {self.year.data} {self.offer_number.data}{self.offer_version.data}.')
                return False

            if hasattr(self, 'id') and offer.id != self.id.data:
                self.submit.errors.append(
                    f'Istnieje już oferta {self.year.data} {self.offer_number.data}{self.offer_version.data}.')
                return False

        return True


class NewOfferForm(OfferForm):
    user = SelectField('Kierownik', coerce=int)
    submit = SubmitField('Utwórz ofertę')


class EditOfferForm(OfferForm):
    id = IntegerField()
    client = SelectField('Klient', coerce=int)
    user = SelectField('Kierownik', coerce=int)
    submit = SubmitField('Zapisz')


class DeleteOfferForm(FlaskForm):
    submit = SubmitField('Usuń')
