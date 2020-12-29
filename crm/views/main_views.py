from flask import Blueprint, render_template

from crm import login_manager
from ..models import User
from ..utils import Settings

bp_main = Blueprint('main', __name__, url_prefix='/')


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@bp_main.route('/')
def home():
    if Settings.get_instance().settings['STANDARD_FOLDER_PATH'] == '':
        return render_template('index.html', init_view=True)
    return render_template('index.html', init_view=False)