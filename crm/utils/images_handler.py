import os
import re

from flask import send_from_directory
from werkzeug.utils import secure_filename

from crm import Settings
from . import FolderHandler
from ..models import Offer

path = os.path.abspath(os.path.dirname(__file__))


def save_image_uploads(images, note, user_initials):
    if Settings.get_instance().settings['CREATE'] == 'Nie' or note.offer_id is None:
        uploads_path = os.path.join(FolderHandler.get_user_folder_path(user_initials), '1.Zdjęcia')
        base_file_name = user_initials
    else:
        offer = Offer.get_by_id(note.offer_id)

        uploads_path = FolderHandler.get_img_folder_path(offer)
        base_file_name = '_'.join([str(offer.year), str(offer.offer_number), offer.offer_version])

    joined_files_names = ''
    for i, img in enumerate(images.data):

        file_name = '_'.join([base_file_name, str(note.id), str(i), img.filename])

        file_name = secure_filename(file_name)
        img.save(os.path.join(uploads_path, file_name))

        joined_files_names += ',' + file_name

    return joined_files_names[1:]


def load_image_uploads(filename):
    user_initial_pattern = re.compile(r'([A-Z]){1,5}')
    filename_parts = filename.split('_')

    if user_initial_pattern.match(filename_parts[0]):
        uploads_path = os.path.join(FolderHandler.get_user_folder_path(filename_parts[0]), '1.Zdjęcia')
    else:
        offer = Offer(year=filename_parts[0], offer_number=filename_parts[1], offer_version=filename_parts[2])
        uploads_path = FolderHandler.get_img_folder_path(offer)

    return send_from_directory(uploads_path, filename)


def get_image_list(note):
    return note.image.split(',')


def delete_images(note):
    user_initial_pattern = re.compile(r'([A-Z]){1,5}')
    images_list = get_image_list(note)

    for image in images_list:
        filename_parts = image.split('_')

        if user_initial_pattern.match(filename_parts[0]):
            uploads_path = os.path.join(FolderHandler.get_user_folder_path(filename_parts[0]), '1.Zdjęcia')
        else:
            offer = Offer(year=filename_parts[0], offer_number=filename_parts[1], offer_version=filename_parts[2])
            uploads_path = FolderHandler.get_img_folder_path(offer)

        image_path = os.path.join(uploads_path, image)
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print("The file does not exist")
