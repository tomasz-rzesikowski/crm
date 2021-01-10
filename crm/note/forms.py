from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, StringField, HiddenField, TextAreaField, MultipleFileField, \
    DateField, BooleanField
from wtforms.validators import DataRequired, length, Optional, InputRequired


class NoteForm(FlaskForm):
    title = StringField('Tytuł', validators=[
        InputRequired(message='Pole jest wymagane.'),
        DataRequired(message='Pole jest wymagane.'),
        length(min=1, max=40, message='Tytuł jest za długi.')
    ])

    description = TextAreaField('Treść notatki', validators=[
        InputRequired(message='Pole jest wymagane.'),
        DataRequired(message='Pole jest wymagane.'),
    ])

    images = MultipleFileField('Zdjęcia', validators=[FileAllowed(['jpeg', 'jpg', 'png'], message='Tylko zdjęcia.')])
    expire_date = DateField('Data zakończenia', validators=[Optional()])
    on_todo_list = BooleanField('Dodać do listy zadań?')

    submit = SubmitField()


class NewNoteForm(NoteForm):
    submit = SubmitField('Utwórz notatkę')


class EditNoteForm(NoteForm):
    id = HiddenField()
    submit = SubmitField('Zapisz')


class DeleteNoteForm(FlaskForm):
    delete_images = BooleanField('Usunąć zdjęcia?')
    submit = SubmitField('Usuń')
