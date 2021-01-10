from flask import Blueprint, render_template, url_for, request
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import redirect

from .forms import LoginForm
from ..user import User

bp_auth = Blueprint('auth', __name__, template_folder='templates')


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_initials(form.initials.data)

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        return render_template('login.html', form=form, title='Logowanie')
    return render_template('login.html', form=form, title='Logowanie')


@bp_auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))
