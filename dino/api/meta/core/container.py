import json
import logging as log

from pprint import pprint

from dino_backend.dino.api.meta.core.entity import Entity
from dino_backend.dino.api.meta.core.exception import PropertyNotFound
from dino_backend.dino.api.meta.util import isempty


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

    def __repr__(self):
        return str(self)

    def get(self, key):
        if hasattr(self.entity_hook, str(key)):
            return getattr(self.entity_hook, str(key))
        raise PropertyNotFound("Unknown property of entity \'{}\': \'{}\'.\n"
                               "List of available properties for entitiy \'{}\': "
                               "{}".format(str(self.entity_hook), key, self.entity_hook, self.entity_hook.get_properties()))

    def serialize(self):
        return json.dumps(self.entity_hook.json_dict)

    def pretty_print(self):
        pprint(self.entity_hook.json_dict, indent=4)

    def iter_json_items(self, _json):
        if isinstance(_json, dict):
            for k, v in _json.items():
                if isinstance(v, dict):
                    yield from self.iter_json_items(_json=v)
                elif isinstance(v, list):
                    yield from self.iter_json_items(_json=v)
                else:
                    yield k, v
        elif isinstance(_json, list):
            for d in _json:
                yield from self.iter_json_items(_json=d)

    def set_empty_values(self, new_value):
        self.__set_empty_values(self.entity_hook.json_dict, new_value)

    def __set_empty_values(self, iterable, new_val):
        if isinstance(iterable, dict):
            for k, v in iterable.items():
                if isinstance(v, dict):
                    self.__set_empty_values(iterable=v, new_val=new_val)
                elif isinstance(v, list):
                    self.__set_empty_values(iterable=v, new_val=new_val)
                else:
                    if isinstance(v, str):
                        if isempty(v):
                            iterable[k] = new_val
        elif isinstance(iterable, list):
            for l in iterable:
                self.__set_empty_values(iterable=l, new_val=new_val)

    def __load_json(self, path=None, fileio=None):
        if path is not None:
            with open(path, 'r', encoding='latin-1') as dat:
                return json.load(dat)
        elif fileio is not None:
            return json.load(fileio)
        return {}
