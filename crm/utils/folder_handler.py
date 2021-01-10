import os
import shutil

from ..settings import Settings


class FolderHandler:
    __instance = None

    @staticmethod
    def create_user_folder(user_initials):
        folder_path = os.path.join(FolderHandler.get_user_folder_path(user_initials),
                                   '1.Zdjęcia')

        if os.path.isdir(folder_path) is False:
            try:
                os.makedirs(folder_path)
            except OSError:
                print("Creation of the directory %s failed" % folder_path)

    @staticmethod
    def get_user_folder_path(user_initials):
        basedir = Settings.get_instance().settings['CONFIG_FOLDER_PATH']

        folder_path = os.path.join(basedir,
                                   user_initials)

        return folder_path

    @staticmethod
    def create_offer_folder(offer):
        if Settings.get_instance().settings['CREATE'] == 'True':
            basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']
            standard_dir = os.path.join(Settings.get_instance().settings['STANDARD_FOLDER_PATH'], '_STANDARD')

            folder_path = os.path.join(basedir,
                                       str(offer.year),
                                       str(offer.offer_number))

            if os.path.isdir(folder_path) is False:
                try:
                    shutil.copytree(standard_dir, folder_path)
                except OSError:
                    print("Creation of the directory %s failed" % folder_path)

            folder_path = os.path.join(folder_path, '2.Oferty', str(offer.offer_version))

            if os.path.isdir(folder_path) is False:
                try:
                    os.makedirs(folder_path)
                except OSError:
                    print("Creation of the directory %s failed" % folder_path)

    @staticmethod
    def delete_offer_folder(offer):
        if Settings.get_instance().settings['CREATE'] == 'True':
            basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']

            folder_path = os.path.join(basedir, str(offer.year), str(offer.offer_number), '2.Oferty',
                                       str(offer.offer_version))
            if os.path.isdir(folder_path):
                try:
                    shutil.rmtree(folder_path, onerror=OSError)
                except OSError:
                    print("Removing of the directory %s failed" % folder_path)

    @staticmethod
    def find_offer_folder(offer):
        if Settings.get_instance().settings['CREATE'] == 'True':
            folder_path = FolderHandler.get_offer_folder_path(offer)

            return os.path.isdir(folder_path)
        return False

    @staticmethod
    def get_offer_folder_path(offer):
        basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']

        folder_path = os.path.join(basedir, str(offer.year),
                                   str(offer.offer_number), '2.Oferty',
                                   str(offer.offer_version))

        return folder_path

    @staticmethod
    def get_img_folder_path(offer):
        if FolderHandler.find_offer_folder(offer):
            basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']

            img_folder_patch = os.path.join(basedir, str(offer.year),
                                            str(offer.offer_number), '1.Info', '1.Zdjęcia')

            return img_folder_patch

        return Settings.get_instance().settings['MAIN_FOLDER_PATH']

    @staticmethod
    def get_instance():
        """ Static access method. """
        if FolderHandler.__instance is None:
            FolderHandler()
        return FolderHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if FolderHandler.__instance is not None:
            raise Exception("This class is a FolderHandler!")
        else:
            FolderHandler.__instance = self
