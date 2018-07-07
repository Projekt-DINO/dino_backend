import os
import json


"""
This class loads and provides access to settings.cfg
"""
class APIConfig(object):

    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))+'/settings.cfg'
        self.config = self.get_config()
        print(self.path)

    """
    Called when self.attr is called.
    
    Modified __getattr__ method to also make it possible to return keys used in settings.cfg
    """
    def __getattr__(self, attr):
        attr = str(attr)
        if attr not in self.config:
            return self.__dict__.__getitem__(attr)
        return self.config[attr]

    """
    Called when str(APIConfig) is used.
    """
    def __str__(self):
        return str(self.config)

    """
    Load the settings.cfg file.
    """
    def get_config(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError('settings.cfg file not found.')
        with open(self.path, 'r') as cfg:
            return json.load(cfg)
