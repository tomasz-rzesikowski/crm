import os
import shutil

from .settings import Settings


class FileHandler:
    __instance = None

    @staticmethod
    def create_offer_file(offer):
        basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']

        file = os.path.join(basedir, str(offer.year), str(offer.offer_number), str(offer.offer_version))
        if os.path.isdir(file) is False:
            try:
                os.makedirs(file)
            except OSError:
                print("Creation of the directory %s failed" % file)

    @staticmethod
    def delete_offer_file(offer):
        basedir = Settings.get_instance().settings['MAIN_FOLDER_PATH']

        file = os.path.join(basedir, str(offer.year), str(offer.offer_number), str(offer.offer_version))
        if os.path.isdir(file) is False:
            try:
                shutil.rmtree(file, onerror=OSError)
            except OSError:
                print("Removing of the directory %s failed" % file)

    @staticmethod
    def get_instance():
        """ Static access method. """
        if FileHandler.__instance is None:
            FileHandler()
        return FileHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if FileHandler.__instance is not None:
            raise Exception("This class is a Settings!")
        else:
            FileHandler.__instance = self
