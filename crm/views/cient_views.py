import os

from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from wtforms import ValidationError

from crm import db
from ..forms import ClientForm
from ..models import Client

bp_client = Blueprint('clients', __name__, url_prefix='/clients')


@bp_client.route('/', methods=['GET'])
def clients():
    clients = Client.get_all()
    return render_template('clients.html', clients=clients)


@bp_client.route('/add', methods=['GET', 'POST'])
def add():
    form = ClientForm(button_label="Dodaj")
    if form.validate_on_submit():
        try:

            form.validate_model()
            form.validate_unique_constrain()

        except ValidationError as error:

            form.button.errors = [error]
            return render_template('add_client.html', form=form)

        else:
            form = ClientForm(button_label="Dodaj")
            name = form.name.data
            surname = form.surname.data
            company = form.company.data
            address_street_and_number = form.address_street_and_number.data
            address_zipcode_and_city = form.address_zipcode_and_city.data
            phone = form.phone.data
            email = form.email.data
            client = Client(name=name, surname=surname, company=company,
                            address_street_and_number=address_street_and_number,
                            address_zipcode_and_city=address_zipcode_and_city,
                            phone=phone, email=email)

            db.session.add(client)
            db.session.commit()

        return redirect(url_for('clients.clients'))

    return render_template('add_client.html', form=form)


@bp_client.route("/edit/<int:idx>", methods=['GET', 'POST'])
def edit(idx):
    client = Client.get_by_id(idx)
    form = ClientForm(button_label="Zapisz")

    if form.validate_on_submit():
        try:

            form.validate_model()
            form.validate_unique_constrain()

        except ValidationError as error:

            form.button.errors = [error]
            return render_template('edit_client.html', form=form)

        else:
            form = ClientForm(button_label="Zapisz")

            client.name = form.name.data
            client.surname = form.surname.data
            client.company = form.company.data
            client.address_street_and_number = form.address_street_and_number.data
            client.address_zipcode_and_city = form.address_zipcode_and_city.data
            client.phone = form.phone.data
            client.email = form.email.data

            db.session.commit()

            return redirect(url_for('clients.clients'))

    if form.name.data is None and form.surname.data is None \
            and form.phone.data is None and form.email.data is None:
        form.name.data = client.name
        form.surname.data = client.surname
        form.company.data = client.company
        form.address_street_and_number.data = client.address_street_and_number
        form.address_zipcode_and_city.data = client.address_zipcode_and_city
        form.phone.data = client.phone
        form.email.data = client.email

    return render_template('edit_client.html', form=form)


@bp_client.route("/delete/<int:idx>", methods=['GET'])
def delete(idx):
    client = Client.get_by_id(idx)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients.clients'))
