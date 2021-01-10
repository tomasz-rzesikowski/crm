from flask import Blueprint, render_template, url_for, request
from flask_login import login_required
from werkzeug.utils import redirect

from crm import db
from .forms import NewClientForm, EditClientForm
from .models import Client

bp_client = Blueprint('client', __name__, template_folder='templates')


@bp_client.route('/', methods=['GET'])
@login_required
def clients():
    clients = Client.get_all()
    return render_template('clients.html', clients=clients)


@bp_client.route('/<idx>', methods=['GET'])
@login_required
def client(idx):
    client = Client.get_by_id(idx)
    return render_template('client.html', client=client)


@bp_client.route('/add', methods=['GET', 'POST'])
@login_required
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

        return redirect(url_for('client.clients'))
    return render_template('add_client.html', form=form)


@bp_client.route("/edit/<int:idx>", methods=['GET', 'POST'])
@login_required
def edit(idx):
    client = Client.get_by_id(idx)
    form = EditClientForm(obj=client)

    if form.validate_on_submit():
        form.populate_obj(client)

        db.session.commit()

        return redirect(url_for('client.clients'))
    return render_template('edit_client.html', form=form)


@bp_client.route("/delete/<int:idx>", methods=['GET'])
@login_required
def delete(idx):
    client = Client.get_by_id(idx)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('client.clients'))
