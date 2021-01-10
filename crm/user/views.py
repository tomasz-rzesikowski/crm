from flask import Blueprint, render_template, url_for, request, abort
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from crm import db
from ..offer import Offer
from ..note import Note
from ..utils import FolderHandler
from .forms import NewUserForm, EditUserForm
from .models import User

bp_user = Blueprint('user', __name__, template_folder='templates')


@bp_user.route('/users', methods=['GET'])
@login_required
def users():
    users = User.get_all()
    return render_template('users.html', users=users, title='Użytkownicy')


@bp_user.route('/', methods=['GET'])
@login_required
def user():
    offers = Offer.get_all_with_client_by_user(current_user.id)
    todos = Note.get_todos(current_user.id)
    return render_template('user.html', offers=offers, notes=todos, title='Strona główna')


@bp_user.route('/add', methods=['GET', 'POST'])
def add():
    form = NewUserForm()

    if form.validate_on_submit():
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    initials=form.initials.data,
                    phone=form.phone.data,
                    email=form.email.data,
                    password=form.password.data)

        FolderHandler.create_user_folder(user.initials)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('user.users'))
    return render_template('add_user.html', form=form, title='Dodawanie użytkownika')


@bp_user.route("/edit/<int:idx>", methods=['GET', 'POST'])
@login_required
def edit(idx):

    user = User.get_by_id(idx)
    if current_user != user:
        abort(403)

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.commit()

        return redirect(url_for('user.users'))
    return render_template('edit_user.html', form=form, title='Edycja użytkownika')


@bp_user.route("/delete/<int:idx>", methods=['GET'])
@login_required
def delete(idx):
    user = User.get_by_id(idx)
    user.status = False
    db.session.commit()
    return redirect(url_for('user.users'))

