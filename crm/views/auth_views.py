from flask import Blueprint, render_template, url_for, request
from flask_login import login_user, logout_user
from werkzeug.utils import redirect

from ..forms import LoginForm
from ..models import User

bp_auth = Blueprint('auth', __name__, url_prefix='/users', template_folder='templates')


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_initials(form.initials.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.home', initials=user.initials))
        return render_template('login.html', login_form=form)
    return render_template('login.html', login_form=form)


@bp_auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))
