from calendar import timegm
from time import gmtime

"""
This file is used to define entities that may
be received by one of the APIs used for gaining
data for our backend.

Each file should contain methods to define easier
access to the respective JSON objects associated
with those entities. Those JSONs almost always
contain any data received by an API (e.g.
OpenRouteServices).

The definition of such methods will help finding
and manage any changes made to one of the external
APIs accessed to gather data for our backend and
the App. It also provides an intuitive way to accessing
relevant JSON keys, in case we need only specific data
from an entity or want to modify something small
without having to loop through the entire JSON just to
find the key.

Every entity MUST be a subclass of the class Entity
(found in entity.py), or else the custom JSON access methods,
along with the JSONContainer class, will not work.
"""


from dino_backend.dino.api.meta.core.entity import Entity


class Route(Entity):
    """
    Route entity.

    Class used for any JSON retrieved from from
    the OpenRouteService routes endpoint.
    """

    def __init__(self, json_dict):
        json_dict["dino"] = {}
        json_dict["dino"]["route_id"] = -1
        json_dict["dino"]["completed_amt"] = -1
        json_dict["dino"]["user_rating"] = -1
        json_dict["dino"]["is_approved"] = -1
        json_dict["dino"]["is_user_made"] = -1
        json_dict["dino"]["is_featured"] = -1
        super(Route, self).__init__(self, json_dict)

    @classmethod
    def __str__(cls):
        return Route.__name__

    @property
    def route_id(self):
        return self.json_dict["dino"]["route_id"]

    @route_id.setter
    def route_id(self, value):
        if value is not None:
            self.json_dict["dino"]["route_id"] = value

    @property
    def completed_amt(self):
        return self.json_dict["dino"]["completed_amt"]

    @completed_amt.setter
    def completed_amt(self, value):
        if value is not None:
            self.json_dict["dino"]["completed_amt"] = value

    @property
    def user_rating(self):
        return self.json_dict["dino"]["user_rating"]

    @user_rating.setter
    def user_rating(self, value):
        if value is not None:
            self.json_dict["dino"]["user_rating"] = value

    @property
    def is_approved(self):
        return self.json_dict["dino"]["is_approved"]

    @is_approved.setter
    def is_approved(self, value):
        if value is not None:
            self.json_dict["dino"]["is_approved"] = value

    @property
    def is_user_made(self):
        return self.json_dict["dino"]["is_user_made"]

    @is_user_made.setter
    def is_user_made(self, value):
        if value is not None:
            self.json_dict["dino"]["is_user_made"] = value

    @property
    def is_featured(self):
        return self.json_dict["dino"]["is_featured"]

    @is_featured.setter
    def is_featured(self, value):
        if value is not None:
            self.json_dict["dino"]["is_featured"] = value

    @property
    def polyline(self):
        return self.json_dict["features"][0]["geometry"]["coordinates"]

    @property
    def distance(self):
        return self.json_dict["features"][0]["properties"]["summary"][0]["distance"]

    @property
    def duration(self):
        return self.json_dict["features"][0]["properties"]["summary"][0]["duration"]

    @property
    def bbox(self):
        return self.json_dict["features"][0]["properties"]["bbox"]

    @property
    def segments(self):
        return self.json_dict["features"][0]["properties"]["segments"]

    @property
    def profile(self):
        return self.json_dict["info"]["query"]["profile"]

    @property
    def language(self):
        return self.json_dict["info"]["query"]["language"]

    @property
    def units(self):
        return self.json_dict["info"]["query"]["units"]

    @property
    def timestamp(self):
        return self.json_dict["info"]["timestamp"]


class PointOfInterest(Entity):

    def __init__(self, json_dict):
        json_dict["features"][0]["info"] = {}
        json_dict["features"][0]["info"]["poi_id"] = -1
        json_dict["features"][0]["info"]["checkpoint"] = -1
        json_dict["features"][0]["info"]["timestamp"] = timegm(gmtime())
        json_dict["features"][0]["properties"]["open_hours"] = {}
        super(PointOfInterest, self).__init__(self, json_dict)

    @classmethod
    def __str__(cls):
        return PointOfInterest.__name__

    @property
    def poi_id(self):
        return self.json_dict["features"][0]["info"]["poi_id"]

    @poi_id.setter
    def poi_id(self, value):
        if value is not None:
            self.json_dict["features"][0]["info"]["poi_id"] = value

    @property
    def checkpoint(self):
        return self.json_dict["features"][0]["info"]["checkpoint"]

    @checkpoint.setter
    def checkpoint(self, value):
        if value is not None:
            self.json_dict["features"][0]["info"]["checkpoint"] = value

    @property
    def timestamp(self):
        return self.json_dict["features"][0]["info"]["timestamp"]

    @property
    def open_hours(self):
        return self.json_dict["features"][0]["properties"]["open_hours"]

    @open_hours.setter
    def open_hours(self, value):
        if value is not None:
            self.json_dict["features"][0]["properties"]["open_hours"] = value

    @property
    def coordinates(self):
        return self.json_dict["features"][0]["geometry"]["coordinates"]

    @property
    def bbox(self):
        return self.json_dict["bbox"]

    @property
    def name(self):
        return self.json_dict["features"][0]["properties"]["name"]

    @property
    def country(self):
        return self.json_dict["features"][0]["properties"]["country"]

    @property
    def country_a(self):
        return self.json_dict["features"][0]["properties"]["country_a"]

    @property
    def region(self):
        return self.json_dict["features"][0]["properties"]["region"]

    @property
    def region_a(self):
        return self.json_dict["features"][0]["properties"]["region_a"]

    @property
    def macrocounty(self):
        return self.json_dict["features"][0]["properties"]["macrocounty"]

    @property
    def county(self):
        return self.json_dict["features"][0]["properties"]["county"]

    @property
    def locality(self):
        return self.json_dict["features"][0]["properties"]["locality"]

    @property
    def label(self):
        return self.json_dict["features"][0]["properties"]["label"]
