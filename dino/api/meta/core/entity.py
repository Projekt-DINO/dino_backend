import logging as log

"""
Entity class.

This is basically a wrapper class which adds behavior to 
any entity class defined in entity_objects.py

Entity, however, cannot exist without an class from entity_objects.py
"""
class Entity(object):

    def __init__(self, entity, json_dict):
        assert json_dict is not None, "json_dict param in class Container mustn't be None"
        assert entity is not None, "entity param in class Container mustn't be None"

        # associated entity found in entity_object.py
        # this cannot be empty
        self.entity = entity

        # the JSON object used in this class
        self.json_dict = json_dict

    """
    Called when str(Entity) is used
    """
    def __str__(self):
        return self.entity.__class__.__name__

    """
    Called when self.attr = value is used.
    
    Blocks modification of entity value to prevent accidental desync with json_dict.
    """
    def __setattr__(self, attr, value):
        if attr == "entity" and hasattr(self, 'entity'):
            log.warning("Modification of entity attribute is not permitted after JSON data has been loaded.")
            return False
        super(Entity, self).__setattr__(attr, value)
        return True

    """
    def __getitem__(self, key):
        key = key.lower()
        if key in self.json_dict['properties']:
            if key in self.get_entity_properties():
                return self.json_dict['properties'][key]
        raise PropertyNotFound("Unknown property of entity \'{}\': \'{}\'".format(str(self.entity.__class__.__name__), key))
    """

    """
    Retrieve the names of all properties defined in this class.
    """
    def get_properties(self):
        return [prop for prop in self.entity.__class__.__dict__ if not prop.startswith("__") and not prop.startswith("_")]

    """
    Called with Entity.construct_obj.
    
    Creates an Entity object instantiated with the according entity (from entity_objects.py) and a json_dict
    """
    @classmethod
    def construct_obj(cls, entity: str, json_dict):
        entities = Entity.get_all_classes()
        if Entity.is_known(entity):
            for _cls in entities:
                if _cls.__name__ == entity:
                    return _cls(json_dict)

    """
    Called with Entity.is_known.
    
    Checks if an entity str matches one of the class names in entity_objects.py
    """
    @classmethod
    def is_known(cls, value):
        entities = Entity.get_all_classes()
        if isinstance(value, str):
            return value in [e.__name__ for e in entities]
        else:
            return value in entities

    """
    Called with Entity.get_all_classes.
    
    Returns all subclasses of Entity. 
    """
    @classmethod
    def get_all_classes(cls):
        return vars()['cls'].__subclasses__()
