import json

from pprint import pprint

from dino_backend.dino.api.meta.core.exception import PropertyNotFound
from dino_backend.dino.api.meta.util import isempty, is_dir, is_file
from dino_backend.dino.api.meta.core.standards.entity_objects import *


"""
JSON Wrapper class.

This class should be used with any JSON we are
working with in the Backend. 

It provides methods to load data from a fileIO 
or an API, along with utility methods to make
working with the JSONs easier.
"""
class JSONContainer(object):

    """
    **kwargs:

        - at least one of: ["fileio", "path", "json"]
    """
    def __init__(self, entity, **kwargs):
        # with open("xy", "r" as data; where data is the fileio object used here
        if 'fileio' in kwargs:
            json_dict = self.__load_json(fileio=kwargs['fileio'])

        # path is just any path on your computer to the file the JSON should be loaded from
        elif 'path' in kwargs:
            if self.__validate_path(kwargs['path']):
                json_dict = self.__load_json(path=kwargs['path'])

        # if the json object already exists, it can be loaded here
        elif 'json' in kwargs:
            json_dict = self.__validate_json(kwargs['json'])
        else:
            raise ValueError("JSONContainers must have data to read JSON from upon initialization.\n"
                             "Use \'fileio\' or \'path\' to indicate where to load it from or pass"
                             "a JSON object.")

        # object hook to the entity class the JSON is associated with (to standardize and simplify access to the JSON)
        # (this is why each entity in entity_object.py must be subclassed from class Entity in entity.py
        self.entity_hook = Entity.construct_obj(entity, json_dict)

    """
    Called when str(JSONContainerObj) is used.
    """
    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.entity_hook))

    """
    Called when print(JSONContainerObj) is used
    """
    def __repr__(self):
        return str(self)

    @classmethod
    def make_api_route_container(cls, **kwargs):
        return JSONContainer(Route.__str__(), **kwargs)

    @classmethod
    def make_poi_container(cls, **kwargs):
        return JSONContainer(PointOfInterest.__str__(), **kwargs)

    """
    Each JSON still offers the option to access keys via key access syntax, e.g. myjson["key1"]["key2"].
    
    get(key) provides the possibility to access the property methods defined for each entity in entity_object.py, to
    make access easier.
    
    The way this works is:
    
        - Assume we have a JSONContainer class with an entity_hook pointing to Entity in entity.py
        - Entity.construct_obj() has instantiated an Entity object in a way that the associated entity (e.g. Route
          in entity_objects.py) was used to create the Entity object
        - By instantiating Entity from the Route entity class, we essentially created a class which points to
          a Route entity (henceforth it is a RouteEntity)
        - RouteEntity now defines property methods in entity_object.py, like polyline and distance
        - By using get("polyline") here, we effectively access the polyline method in RouteEntity
        
    (Thank you dynamic paradigm)
    """
    def get(self, key):
        if key in self.entity_hook.get_properties():
            return getattr(self.entity_hook, str(key))
        raise PropertyNotFound("Unknown property of entity \'{}\': \'{}\'.\n"
                               "List of available properties for entitiy \'{}\': "
                               "{}".format(str(self.entity_hook), key, self.entity_hook, self.entity_hook.get_properties()))

    def set(self, key, val):
        if key in self.entity_hook.get_properties():
            setattr(self.entity_hook, str(key), val)
            return True
        raise PropertyNotFound("Unknown property of entity \'{}\': \'{}\'.\n"
                               "List of available properties for entitiy \'{}\': "
                               "{}".format(str(self.entity_hook), key, self.entity_hook, self.entity_hook.get_properties()))

    def get_container_entity_type(self):
        return str(self.entity_hook)

    """
    Dump the JSON object as a string, serializing it in the process.
    """
    def serialize(self):
        return json.dumps(self.entity_hook.json_dict)

    """
    Prettyprint the JSON object, for testing purposes.
    """
    def pretty_print(self):
        pprint(self.entity_hook.json_dict, indent=4)

    """
    JSONContainer itself does not hold the JSON, entity_hook does.
    """
    def as_json(self):
        return self.entity_hook.json_dict

    """
    Retrieve the entity JSON reduced to the properties defined in the respective entity_object.py class.
    
    Note that this should NOT override the current JSON. This should always return a new JSON object.
    """
    def as_standardized_json(self):
        return {prop: self.get(prop) for prop in self.entity_hook.__class__.__dict__ if not prop.startswith("__") and not prop.startswith("_")}

    """
    Generator function.
    
    Iterate through all key:value pairs that exist in the JSON, no matter how deeply nested they are. 
    """
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

    """
    DynamoDB complains if a string value in a table is empty, i.e. "".
    
    This method is used to replace all empty values with a new_value, e.g. "None" or "Null"
    """
    def replace_empty_values(self, new_value):
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

    """
    Method to load a json from a path or fileio.
    """
    def __load_json(self, path=None, fileio=None):
        if path is not None:
            with open(path, 'r', encoding='latin-1') as dat:
                return json.load(dat)
        elif fileio is not None:
            return json.load(fileio)
        raise OSError("Unknown error while loading JSON file.")

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
            raise ValueError("JSON object can't be None")
        if isinstance(obj, str):
            return json.loads(obj, encoding="utf-8")
        if isinstance(obj, dict):
            return obj
