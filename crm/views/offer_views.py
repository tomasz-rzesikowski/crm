from flask import Blueprint, render_template, redirect, url_for
from wtforms import ValidationError

from crm import db
from ..forms import OfferForm
from ..models import Offer

bp_offer = Blueprint('offers', __name__, url_prefix='/offers')


@bp_offer.route('', methods=['GET'])
def offers():
    offers = Offer.get_all()
    return render_template('offers.html', offers=offers)


@bp_offer.route('/add', methods=['GET', 'POST'])
def add():
    form = OfferForm(button_label="Dodaj")
    if form.validate_on_submit():
        try:
            form.validate_unique_constrain()
        except ValidationError as error:
            form.button.errors = [error]
            return render_template('add_offer.html', form=form)

        form = OfferForm(button_label="Dodaj")
        year = form.year.data
        offer_number = form.offer_number.data
        offer_version = form.offer_version.data

        offer = Offer(year=year, offer_number=offer_number, offer_version=offer_version)

        db.session.add(offer)
        db.session.commit()
        return redirect(url_for('offers.offers'))

    return render_template('add_offer.html', form=form)


@bp_offer.route("/edit/<int:idx>", methods=['GET', 'POST'])
def edit(idx):
    offer = Offer.get_by_id(idx)
    form = OfferForm(button_label="Zapisz", base_idx=idx)
    if form.validate_on_submit():
        try:
            form.validate_unique_constrain()
        except ValidationError as error:
            form.button.errors = [error]
            return render_template('edit_offer.html', form=form)

        form = OfferForm(button_label="Zapisz", base_idx=idx)

        offer = Offer.get_by_id(idx)
        offer.year = form.year.data
        offer.offer_number = form.offer_number.data
        offer.offer_version = form.offer_version.data

        db.session.commit()

        return redirect(url_for('offers.offers'))

    if form.year.data is None:
        form.year.data = offer.year
        form.offer_number.data = offer.offer_number
        form.offer_version.data = offer.offer_version

    return render_template('edit_offer.html', form=form)


@bp_offer.route("/delete/<int:idx>", methods=['GET'])
def delete(idx):
    offer = Offer.get_by_id(idx)
    db.session.delete(offer)
    db.session.commit()
    return redirect(url_for('offers.offers'))
