from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from ..settings import Settings

bp_main = Blueprint('main', __name__, template_folder='templates')


@bp_main.route('/')
def index():
    if Settings.get_instance().settings['STANDARD_FOLDER_PATH'] == '':
        return render_template('index.html', init_view=True)

    if current_user.is_authenticated:
        return redirect(url_for('user.user'))

    return render_template('index.html', init_view=False)
