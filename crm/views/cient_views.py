from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect

from crm import db
from ..forms import NewClientForm, EditClientForm
from ..models import Client

bp_client = Blueprint('clients', __name__, url_prefix='/clients')


@bp_client.route('/', methods=['GET'])
def clients():
    clients = Client.get_all()
    return render_template('clients.html', clients=clients)


@bp_client.route('/<idx>', methods=['GET'])
def client(idx):
    client = Client.get_by_id(idx)
    return render_template('client.html', client=client)


@bp_client.route('/add', methods=['GET', 'POST'])
def add():
    form = NewClientForm()

    if form.validate_on_submit():
        client = Client(name=form.name.data,
                        surname=form.surname.data,
                        company=form.company.data,
                        address_street_and_number=form.address_street_and_number.data,
                        address_zipcode_and_city=form.address_zipcode_and_city.data,
                        phone=form.phone.data,
                        email=form.email.data)

        db.session.add(client)
        db.session.commit()

        return redirect(url_for('clients.clients'))

    return render_template('add_client.html', form=form)


@bp_client.route("/edit/<int:idx>", methods=['GET', 'POST'])
def edit(idx):
    client = Client.get_by_id(idx)
    form = EditClientForm()

    if request.method == 'GET':
        form.id.data = client.id
        form.name.data = client.name
        form.surname.data = client.surname
        form.company.data = client.company
        form.address_street_and_number.data = client.address_street_and_number
        form.address_zipcode_and_city.data = client.address_zipcode_and_city
        form.phone.data = client.phone
        form.email.data = client.email

    if form.validate_on_submit():
        client.name = form.name.data
        client.surname = form.surname.data
        client.company = form.company.data
        client.address_street_and_number = form.address_street_and_number.data
        client.address_zipcode_and_city = form.address_zipcode_and_city.data
        client.phone = form.phone.data
        client.email = form.email.data

        db.session.commit()

        return redirect(url_for('clients.clients'))

    return render_template('edit_client.html', form=form)


@bp_client.route("/delete/<int:idx>", methods=['GET'])
def delete(idx):
    client = Client.get_by_id(idx)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients.clients'))
