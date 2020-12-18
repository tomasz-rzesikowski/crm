import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings:
    __instance = None

    def read(self):
        with open(os.path.join(basedir, 'settings.txt'), "r") as f:
            for line in f:
                setting = line.rstrip().split('=')
                self.settings[setting[0]] = setting[1]

    def save_to_file(self):
        with open(os.path.join(basedir, 'settings.txt'), "w") as f:
            for key, value in self.settings.items():
                f.write(f'{key}={value}\n')

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Settings.__instance is None:
            Settings()
        return Settings.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Settings.__instance is not None:
            raise Exception("This class is a Settings!")
        else:
            Settings.__instance = self
            self.settings = {'MAIN_FOLDER_PATH': '',
                             'DB_PATH': ''}
            self.read()
