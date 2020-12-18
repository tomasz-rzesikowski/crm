from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    main_folder_path = StringField(
        'Ścieżka do głównego folderu',
        validators=[DataRequired()]
    )

    db_location = StringField(
        'Ścieżka do głównego folderu',
        validators=[DataRequired()]
    )

    create_folders = RadioField('Tworzyć i usuwać foldery na dysku?', choices=['Tak', 'Nie'])

    submit = SubmitField('Zapisz')
