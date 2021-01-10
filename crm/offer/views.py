from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from crm import db
from ..utils import FolderHandler
from ..user import User
from .forms import NewOfferForm
from .models import Offer

bp_offer = Blueprint('offer', __name__, template_folder='templates')


@bp_offer.route('', methods=['GET'])
@login_required
def offers():
    offers = Offer.get_all_with_user_and_client()
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

        FolderHandler.create_offer_folder(offer)

        return redirect(url_for('offer.offers'))
    return render_template('add_offer.html', form=form)


@bp_offer.route("/delete/<int:idx>", methods=['GET'])
@login_required
def delete(idx):
    offer = Offer.get_by_id(idx)

    db.session.delete(offer)
    db.session.commit()

    FolderHandler.delete_offer_folder(offer)

    return redirect(url_for('offer.offers'))
