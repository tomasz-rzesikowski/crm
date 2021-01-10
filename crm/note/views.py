from flask import Blueprint, render_template, url_for, request, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from crm import db
from ..utils.images_handler import save_image_uploads, get_image_list, load_image_uploads, delete_images

from .forms import NewNoteForm, DeleteNoteForm
from .models import Note

bp_note = Blueprint('note', __name__, template_folder='templates')


@bp_note.route('uploads/<filename>')
def uploads(filename):
    return load_image_uploads(filename)


@bp_note.route('/', methods=['GET'])
@login_required
def notes():
    notes = Note.get_all_with_users()
    return render_template('notes.html', notes=notes)


@bp_note.route('/<idx>', methods=['GET'])
@login_required
def note(idx):
    note = Note.get_by_id_with_user(idx)
    form = DeleteNoteForm()
    image_list = get_image_list(note)

    return render_template('note.html', note=note, form=form, image_list=image_list)


@bp_note.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = NewNoteForm()

    if form.validate_on_submit():

        note = Note(title=form.title.data,
                    description=form.description.data,
                    user_id=current_user.id,
                    expire_date=form.expire_date.data,
                    on_todo_list=form.on_todo_list.data)

        if request.args.get('client_id', default=False, type=int):
            note.client_id = request.args.get('client_id')

        if request.args.get('offer_id', default=False, type=int):
            note.offer_id = request.args.get('offer_id')

        db.session.add(note)
        db.session.flush()

        filename = save_image_uploads(form.images, note, current_user.initials)

        note.image = filename

        db.session.commit()

        return redirect(url_for('note.notes'))
    return render_template('add_note.html', form=form)


@bp_note.route("/delete/<int:idx><delete_img>", methods=['GET'])
@login_required
def delete(idx, delete_img):
    note = Note.query.get(idx)

    db.session.delete(note)
    db.session.commit()

    if delete_img:
        delete_images(note)

    return redirect(url_for('note.notes'))
