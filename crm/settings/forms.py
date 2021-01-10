from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, InputRequired


class SettingsForm(FlaskForm):
    main_folder_path = StringField('Ścieżka do głównego folderu', validators=[
        InputRequired(message='Pole jest wymagane.'),
        DataRequired(message='Pole jest wymagane.'),
    ])

    standard_folder_path = StringField('Ścieżka do folderu z folderem _standard', validators=[
        InputRequired(message='Pole jest wymagane.'),
        DataRequired(message='Pole jest wymagane.'),
    ])

    db_location = StringField('Ścieżka do folderu aplikacji', validators=[
        InputRequired(message='Pole jest wymagane.'),
        DataRequired(message='Pole jest wymagane.'),
    ])

    create_folders = BooleanField('Tworzyć i usuwać foldery na dysku?')

    submit = SubmitField('Zapisz')
