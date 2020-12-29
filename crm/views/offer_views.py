from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from crm import db
from ..utils import FileHandler
from ..forms import NewOfferForm
from ..models import User
from ..models import Offer

bp_offer = Blueprint('offers', __name__, url_prefix='/offers')


@bp_offer.route('', methods=['GET'])
@login_required
def offers():
    offers = Offer.get_all_with_users_initials()
    return render_template('offers.html', offers=offers)


@bp_offer.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = NewOfferForm()

    users = User.get_all_initials()
    form.user.choices = users

    if form.validate_on_submit():
        offer = Offer(year=form.year.data,
                      offer_number=form.offer_number.data,
                      offer_version=form.offer_version.data,
                      client_id=request.args.get('client_id'),
                      user_id=form.user.data)

        db.session.add(offer)
        db.session.commit()

        FileHandler.create_offer_file(offer)

        return redirect(url_for('offers.offers'))

    return render_template('add_offer.html', form=form)


@bp_offer.route("/edit/<int:idx>", methods=['GET', 'POST'])
@login_required
def edit(idx):
    return redirect(url_for('offers.offers'))

    # Temporary disabled offer edit. Probably, in the future this option will be permanently removed.

    # offer = Offer.get_by_id(idx)
    # form = EditOfferForm()
    #
    # if request.method == 'GET':
    #     form.id.data = offer.id
    #     form.year.data = offer.year
    #     form.offer_number.data = offer.offer_number
    #     form.offer_version.data = offer.offer_version
    #
    # clients = []
    # for client in Client.get_all_names_and_surnames():
    #     clients.append((client[0], client[1] + ' ' + client[2]))
    #
    # form.client.choices = clients
    # if request.method == 'GET':
    #     form.client.data = offer.user_id
    #
    # users = User.get_all_initials()
    # form.user.choices = users
    # if request.method == 'GET':
    #     form.user.data = offer.user_id
    #
    # if form.validate_on_submit():
    #     offer.year = form.year.data
    #     offer.offer_number = form.offer_number.data
    #     offer.offer_version = form.offer_version.data
    #     offer.client_id = form.client.data
    #     offer.user_id = form.user.data
    #
    #     db.session.commit()
    #
    #     return redirect(url_for('offers.offers'))
    #
    # return render_template('edit_offer.html', form=form)


@bp_offer.route("/delete/<int:idx>", methods=['GET'])
@login_required
def delete(idx):
    offer = Offer.get_by_id(idx)
    db.session.delete(offer)
    db.session.commit()

    FileHandler.delete_offer_file(offer)

    return redirect(url_for('offers.offers'))
