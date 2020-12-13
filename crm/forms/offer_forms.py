from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class OfferForm(FlaskForm):
    def __init__(self, button_label, **kwargs):
        super(OfferForm, self).__init__(**kwargs)
        self.button.label.text = button_label

    form_fields = ['year', 'offer_number', 'button']

    year = IntegerField('Rok', validators=[DataRequired()])
    offer_number = IntegerField('Numer oferty', validators=[DataRequired()])
    button = SubmitField()
