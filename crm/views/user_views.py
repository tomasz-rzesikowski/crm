from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from crm import db
from ..forms import NewUserForm, EditUserForm
from ..models import User

bp_user = Blueprint('users', __name__, url_prefix='/users', template_folder='templates')


@bp_user.route('/', methods=['GET'])
def users():
    users = User.get_all()
    return render_template('users.html', users=users)


@bp_user.route('/add', methods=['GET', 'POST'])
def add():
    form = NewUserForm()

    if form.validate_on_submit():
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    initials=form.initials.data,
                    phone=form.phone.data,
                    email=form.email.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('users.users'))

    return render_template('add_user.html', form=form)


@bp_user.route("/edit/<int:idx>", methods=['GET', 'POST'])
def edit(idx):
    user = User.get_by_id(idx)
    form = EditUserForm()

    form.id.data = user.id
    form.name.data = user.name
    form.surname.data = user.surname
    form.initials.data = user.initials
    form.phone.data = user.phone
    form.email.data = user.email

    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.initials = form.initials.data
        user.phone = form.phone.data
        user.email = form.email.data

        db.session.commit()

        return redirect(url_for('users.users'))

    return render_template('edit_user.html', form=form)


@bp_user.route("/delete/<int:idx>", methods=['GET'])
def delete(idx):
    user = User.get_by_id(idx)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.users'))
