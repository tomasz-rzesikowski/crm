from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from crm import db
from ..forms import UserForm
from ..models import User

bp_user = Blueprint('users', __name__, url_prefix='/users', template_folder='templates')


@bp_user.route('/', methods=['GET'])
def users():
    users = User.get_all()
    return render_template('users.html', users=users)


@bp_user.route('/add', methods=['GET', 'POST'])
def add():
    form = UserForm(button_label="Dodaj")
    if form.validate_on_submit():
        form = UserForm(button_label="Dodaj")
        name = form.name.data
        surname = form.surname.data
        initials = form.initials.data
        phone = form.phone.data
        email = form.email.data
        user = User(name=name, surname=surname, initials=initials, phone=phone, email=email)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('users.users'))

    return render_template('add_user.html', form=form)


@bp_user.route("/edit/<int:idx>", methods=['GET', 'POST'])
def edit(idx):
    user = User.get_by_id(idx)
    form = UserForm(button_label="Zapisz", base_idx=idx)

    if form.validate_on_submit():
        form = UserForm(button_label="Zapisz",  base_idx=idx)
        user = User.get_by_id(idx)
        user.name = form.name.data
        user.surname = form.surname.data
        user.initials = form.initials.data
        user.phone = form.phone.data
        user.email = form.email.data

        db.session.commit()

        return redirect(url_for('users.users'))

    if form.name.data is None:
        form.name.data = user.name
        form.surname.data = user.surname
        form.initials.data = user.initials
        form.phone.data = user.phone
        form.email.data = user.email

    return render_template('edit_user.html', form=form)


@bp_user.route("/delete/<int:idx>", methods=['GET'])
def delete(idx):
    user = User.get_by_id(idx)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.users'))
