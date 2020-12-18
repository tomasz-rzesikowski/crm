from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect

from ..settings import Settings
from ..forms import SettingsForm


bp_settings = Blueprint('settings', __name__, url_prefix='/settings')


@bp_settings.route('/', methods=['GET', 'POST'])
def settings():
    settings = Settings.get_instance()
    form = SettingsForm()

    if request.method == 'GET':
        form.main_folder_path.data = settings.settings['MAIN_FOLDER_PATH']
        form.db_location.data = settings.settings['DB_PATH']
        form.create_folders.data = settings.settings['CREATE']

    if form.validate_on_submit():
        settings.settings['MAIN_FOLDER_PATH'] = form.main_folder_path.data
        settings.settings['DB_PATH'] = form.db_location.data
        settings.settings['CREATE'] = form.create_folders.data

        settings.save_to_file()

        return redirect(url_for('settings.settings'))

    return render_template('settings.html', form=form)
