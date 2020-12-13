from flask import Blueprint, render_template, redirect, url_for

from crm import db
from ..forms import OfferForm
from ..models import Offer

bp_offer = Blueprint('offers', __name__, url_prefix='/offers')


@bp_offer.route('', methods=['GET'])
def show_all_offers():
    offers = Offer.get_all()
    return render_template('offers.html', offers=offers)


@bp_offer.route('/add', methods=['GET', 'POST'])
def add_offer():
    form = OfferForm(button_label="Dodaj")
    if form.validate_on_submit():
        form = OfferForm(button_label="Dodaj")
        year = form.year.data
        offer_number = form.offer_number.data

        offer = Offer(year=year, offer_number=offer_number)

        db.session.add(offer)
        db.session.commit()
        return redirect(url_for('offers.show_all_offers'))

    return render_template('add_offer.html', form=form)
