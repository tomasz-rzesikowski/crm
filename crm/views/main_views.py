from flask import Blueprint, render_template

from ..utils import Settings

bp_main = Blueprint('main', __name__, url_prefix='/')


@bp_main.route('/')
def home():
    if Settings.get_instance().settings['STANDARD_FOLDER_PATH'] == '':
        return render_template('index.html', init_view=True)
    return render_template('index.html', init_view=False)