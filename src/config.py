import configparser
import os
import pathlib


class Config:
    def __init__(self):
        self.config_version = "0.1"

        self.config = configparser.ConfigParser()

        self.config_path = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), 'config.txt')

        if not os.path.exists(self.config_path):
            print("Config generated")
            self.generate_defaults()
        else:
            print("Config exists")
            if self.check_config():
                print("     Config failed version check")
                os.remove(self.config_path)
                print("     -> Generating new Config")
                self.generate_defaults()
            else:
                self.read_config()

    def generate_defaults(self):
        self.config['main'] = {
            'version': self.config_version,
            'width': 15,
            'height': 30,
            'orientation': '1'
        }
        self.write_config(self.config)

    def read_config(self):
        print("Config read")
        print(self.config.read(self.config_path))

    def get_config(self):
        return self.config

    def change_config(self, category, name, value):
        self.config[category][name] = value
        self.write_config(self.config)

    def write_config(self, config):
        with open(self.config_path, "w") as configfile:
            config.write(configfile)
            print("Config saved")

    def check_config(self) -> bool:
        if not self.config.has_option('main', 'version'):
            return False

        if self.config['main']['version'] != self.config_version:
            return False

        # TODO: Check if config is complete
        return True