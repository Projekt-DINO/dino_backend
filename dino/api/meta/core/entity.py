import json
import logging as log
import sys

from abc import ABCMeta, abstractmethod
from pprint import pprint

from dino_backend.dino.api.meta.util import upperfirst
from dino_backend.dino.api.meta.core.exception import PropertyNotFound


class Entity(object):

    def __init__(self, entity, json_dict):
        assert json_dict is not None, "json_dict param in class Container mustn't be None"
        assert entity is not None, "entity param in class Container mustn't be None"

        self.entity = entity
        self.json_dict = json_dict
        self.json_serialized = None

    def __str__(self):
        return self.entity.__class__.__name__

    def __setattr__(self, attr, value):
        if attr == "entity" and hasattr(self, 'entity'):
            log.warning("Modification of entity attribute is not permitted after JSON data has been loaded.")
            return False
        self.__dict__[attr] = value
        return True

    """
    def __getitem__(self, key):
        key = key.lower()
        if key in self.json_dict['properties']:
            if key in self.get_entity_properties():
                return self.json_dict['properties'][key]
        raise PropertyNotFound("Unknown property of entity \'{}\': \'{}\'".format(str(self.entity.__class__.__name__), key))
    """

    def __getitem__(self, key):
        if key in self.get_entity_properties():
            return getattr(self.entity, key)()

    def serialize(self):
        if self.json_serialized is not None:
            return self.json_serialized
        self.json_serialized = json.dumps(self.json_dict)
        return self.json_serialized

    def get_entity_properties(self):
        return [prop for prop in self.entity.__class__.__dict__ if not prop.startswith("__") and not prop.startswith("_")]

    def prettyprint_all(self):
        for prop in self.get_entity_properties():
            print(upperfirst(prop), self[prop])
        pprint(self.json_dict, indent=4)

    def prettyprint_json(self):
        pprint(self.json_dict, indent=4)

    @classmethod
    def construct_obj(cls, entity: str, json_dict):
        entities = Entity.get_all_classes()
        if Entity.is_known(entity):
            for _cls in entities:
                if _cls.__name__ == entity:
                    return _cls(json_dict)

    @classmethod
    def is_known(cls, value):
        entities = Entity.get_all_classes()
        if isinstance(value, str):
            return value in [e.__name__ for e in entities]
        else:
            return value in entities

    @classmethod
    def get_all_classes(cls):
        return vars()['cls'].__subclasses__()
