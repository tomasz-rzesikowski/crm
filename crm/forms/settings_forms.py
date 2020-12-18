from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
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

    submit = SubmitField('Zapisz')
