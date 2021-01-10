import os

basedir = os.path.abspath(os.path.dirname(__file__))
settings_path = os.path.join(basedir, '..', '..', 'settings.txt')


class Settings:
    __instance = None

    def read(self):
        with open(settings_path, "r") as f:
            for line in f:
                setting = line.rstrip().split('=')
                self.settings[setting[0]] = setting[1]

    def save_to_file(self):
        with open(settings_path, "w") as f:
            for key, value in self.settings.items():
                f.write(f'{key}={value}\n')
                self.settings[key] = value

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
                             'STANDARD_FOLDER_PATH': '',
                             'CONFIG_FOLDER_PATH': '',
                             'CREATE': 'False'}
            self.read()
