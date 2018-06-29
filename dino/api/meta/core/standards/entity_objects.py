from dino.api.meta.core.entity import Entity


class Route(Entity):

    def __init__(self, json_dict):
        super(Route, self).__init__(self, json_dict)

    @classmethod
    def __str__(cls):
        return Route.__name__

    @property
    def polyline(self):
        return self.json_dict["features"][0]["geometry"]["coordinates"]

    @property
    def distance(self):
        return self.json_dict["features"][0]["properties"]["summary"][0]["distance"]

    @property
    def duration(self):
        return self.json_dict["features"][0]["properties"]["summary"][0]["duration"]


"""
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Old entities
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class Tavern(Entity):

    def __init__(self, json_dict):
        super(Tavern, self).__init__(self, json_dict)

    @classmethod
    def __str__(cls):
        return Tavern.__name__

    @property
    def latitude(self):
        return self['latitude']

    @property
    def longitude(self):
        return self['longitude']

    @property
    def name(self):
        return self['name']

    @property
    def street(self):
        return self['street']

    @property
    def link(self):
        return self['link']

    @property
    def telephone(self):
        return self['telephone']

    @property
    def open_time(self):
        return self['open_time']

    @property
    def close_time(self):
        return self['close_time']

    @property
    def description(self):
        return self['description']


class Toilet(Entity):

    def __init__(self, json_dict):
        super(Toilet, self).__init__(self, json_dict)

    @classmethod
    def __str__(cls):
        return Toilet.__name__

    @property
    def longitude(self):
        return self['longitude']

    @property
    def latitude(self):
        return self['latitude']

    @property
    def name(self):
        return self['name']

    @property
    def open_time(self):
        return self['open_time']

    @property
    def close_time(self):
        return self['close_time']

    @property
    def costs(self):
        return self['costs']

"""""
