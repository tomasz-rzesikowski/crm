import os
import shutil

from .settings import Settings


class FileHandler:
    __instance = None

    @staticmethod
    def create_offer_file(offer):
        if Settings.get_instance().settings['CREATE'] == 'Tak':
            basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']
            standard_dir = os.path.join(Settings.get_instance().settings['STANDARD_FOLDER_PATH'], '_STANDARD')

            file_path = os.path.join(basedir,
                                     str(offer.year),
                                     str(offer.offer_number))

            if os.path.isdir(file_path) is False:
                try:
                    shutil.copytree(standard_dir, file_path)
                except OSError:
                    print("Creation of the directory %s failed" % file_path)

            file_path = os.path.join(file_path, '2.Oferty', str(offer.offer_version))
            
            if os.path.isdir(file_path) is False:
                try:
                    os.makedirs(file_path)
                except OSError:
                    print("Creation of the directory %s failed" % file_path)

    @staticmethod
    def delete_offer_file(offer):
        if Settings.get_instance().settings['CREATE'] == 'Tak':
            basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']

            file_path = os.path.join(basedir, str(offer.year), str(offer.offer_number), '2.Oferty', str(offer.offer_version))
            if os.path.isdir(file_path):
                try:
                    shutil.rmtree(file_path, onerror=OSError)
                except OSError:
                    print("Removing of the directory %s failed" % file_path)

    @staticmethod
    def find_offer_file(offer):
        if Settings.get_instance().settings['CREATE'] == 'Tak':
            basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']

            file_path = os.path.join(basedir, str(offer.year.data),
                                     str(offer.offer_number.data),
                                     str(offer.offer_version.data))

            return os.path.isdir(file_path)
        return False

    @staticmethod
    def get_instance():
        """ Static access method. """
        if FileHandler.__instance is None:
            FileHandler()
        return FileHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if FileHandler.__instance is not None:
            raise Exception("This class is a FileHandler!")
        else:
            FileHandler.__instance = self
