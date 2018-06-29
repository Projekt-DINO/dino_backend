import json as _json

from dino_backend.dino.api.meta.util import is_dir, is_file
from dino_backend.dino.api.meta.core.container import JSONContainer
from dino_backend.dino.api.meta.core.standards.entity_objects import *


class Feeder(object):

    __slots__ = [
        'data_path',
        'json_object',
        'data_container',
    ]

    def __init__(self, path=None, json=None):
        self.data_path = path
        self.json_object = json
        self.data_container = None

    def __str__(self):
        return str(self.__class__.__name__)

    @property
    def path(self):
        return self.data_path

    @path.setter
    def path(self, val):
        if self.__validate_path(val):
            self.data_path = val

    @property
    def json(self):
        return self.json_object

    @json.setter
    def json(self, val):
        self.json_object = self.__validate_json(val)

    def feed_route(self, path=None, json=None):
        if path is not None:
            self.data_path = path
        elif json is not None:
            self.json_object = json
        self.__feed_data(entity=Route.__str__())

    """
    def feed_toilet(self, path=None):
        if path is not None:
            self.data_path = path
        self.__feed_data(entity=Toilet.__str__())

    def feed_tavern(self, path=None):
        if path is not None:
            self.data_path = path
        self.__feed_data(entity=Tavern.__str__())

    def feed_museum(self, path=None):
        if path is not None:
            self.data_path = path
        self.__feed_data(entity=Museum.__str__())
        
    def feed(self, path=None):
        if path is not None:
            self.data_path = path
        self.__feed_data(entity=None)
    """

    def __feed_data(self, entity):
        self.data_container = self.__read_json(entity)
        #TODO: DynamoDB

    def __read_json(self, entity=None):
        if entity is None:
            pass  # TODO: any kind of entity
        if self.data_path is not None:
            return JSONContainer(path=self.data_path, entity=entity)
        elif self.json_object is not None:
            return JSONContainer(json=self.json_object, entity=entity)

    def __read_csv(self, entity=None):
        return None  # TODO: csv to json

    def __validate_path(self, path):
        if not isinstance(path, str):
            raise ValueError("%s must be of type str" % path)
        if is_dir(path):
            raise IsADirectoryError("%s is directory, not a file." % path)
        if not is_file(path):
            raise FileNotFoundError("%s not found." % path)
        return True

    def __validate_json(self, obj):
        if obj is None:
            raise ValueError("json object can't be None")
        if isinstance(obj, str):
            return _json.loads(obj, encoding="utf-8")
        if isinstance(obj, dict):
            return _json.dumps(obj)
