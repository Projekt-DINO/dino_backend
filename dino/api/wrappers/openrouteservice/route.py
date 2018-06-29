import os


class Route(object):
    
    def __init__(self, api_key, **kwargs):
        self.api_key = api_key
        self.parameters = {
            "coordinates": "",              # pipe separated list of lat,long coordinates, e.g. "98.3562,45.253|93.2532,56.3526|82.3525,56.3543"
            "profile": "",                  # must be one of Profiles()
            "preference": "",               # must be one of Preferences()
            "format": "geojson",
            "units": "",                    # must be one of Units()
            "language": "",                 # must be one of Languages()
            "geometry": True,
            "geometry_format": "",
            "geometry_simplify": False,
            "instructions": True,
            "instructions_format": "text",  # text or html
            "roundabout_exists": False,
            "attributes": "", 
            "maneuvers": False,
            "radiuses": "",
            "bearings": "",
            "continue_straight": False,
            "elevation": False,
            "extra_info": "",
            "optimized": True,
            "options": "",
            "id": "",
        }
        if kwargs:
            self.parameters = {**self.parameters, **kwargs}
        
    def build_url(self):
        url = "https://api.openrouteservice.org/directions?api_key={}".format(self.api_key)
        for key, value in self.parameters.items():
            url += "&" + str(key) + "=" + str(value)
        return url


class Profiles:
    """
    Possible values for profile parameter.
    """
    DRIVING_CAR = "driving-car"
    DRIVING_HGV = "driving-hgv"  # HGV = Heavy Goods Vehicle (LKW)
    CYCLING_REGULAR = "cycling-regular"
    CYCLING_ROAD = "cycling-road"
    CYCLING_SAFE = "cycling-safe"
    CYCLING_MOUNTAIN = "cycling-mountain"
    CYCLING_TOUR = "cycling-tour"
    FOOT_WALKING = "foot-walking"
    FOOT_HIKING = "foot-hiking"
    WHEELCHAIR = "wheelchair"


class Preferences:
    """
    Possible values for route preference.
    """
    FASTEST = "fastest"
    SHORTEST = "shortest"
    RECOMMENDED = "recommended"


class Units:
    """
    Possible distance units.
    """
    METERS = "m"
    KILOMETERS = "km"
    MILES = "mi"


class Languages:
    """
    Possible languages for the route instrunctions.
    """
    ENGLISH = "en"
    GERMAN = "de"
    RUSSIAN = "ru"
    DANISH = "dk"
    SPANISH = "es"
    FRENCH = "fr"
    ITALIAN = "it"
    DUTCH = "nl"
    CHINESE = "cn"
    SWEDISH = "se"
    TURKISH = "tr"
    GREEK = "gr"
    BRAZILIAN_PORTUGUESE = "br"
