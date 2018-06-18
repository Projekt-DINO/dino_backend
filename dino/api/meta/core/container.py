import json
import logging as log

from dino_backend.dino.api.meta.core.entity import Entity
from dino_backend.dino.api.meta.core.exception import PropertyNotFound


class JSONContainer(object):

    def __init__(self, entity, **kwargs):
        if 'fileio' in kwargs:
            json_dict = self.__load_json(fileio=kwargs['fileio'])
        elif 'path' in kwargs:
            json_dict = self.__load_json(path=kwargs['path'])
        elif 'json' in kwargs:
            json_dict = kwargs['json']
        else:
            raise ValueError("JSONContainers must have data to read JSON from upon initialization.\n"
                             "Use \'fileio\' or \'path\' to indicate where to load it from or pass"
                             "a JSON object.")
        self.entity_hook = Entity.construct_obj(entity, json_dict)

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.entity_hook))

    def get(self, key):
        if hasattr(self.entity_hook, str(key)):
            return getattr(self.entity_hook, str(key))
        raise PropertyNotFound("Unknown property of entity \'{}\': \'{}\'.\n"
                               "List of available properties for entitiy \'{}\': {}".format(str(self.entity_hook),
                                                                                            key, self.entity_hook,
                                                                                            self.entity_hook.get_entity_properties()))

    def prettyprint(self):
        self.entity_hook.prettyprint_json()

    def prettyprint_all(self):
        self.entity_hook.prettyprint_all()

    def __load_json(self, path=None, fileio=None):
        if path is not None:
            with open(path, 'r', encoding='latin-1') as dat:
                return json.load(dat)
        elif fileio is not None:
            return json.load(fileio)
        return {}
