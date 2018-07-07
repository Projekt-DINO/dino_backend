"""

This entire file is not used.


"""


class PointOfInterest(object):

    # TODO: POI Category IDs
    
    def __init__(self, api_key, geometry, filters=None, request=None):
        self.api_key = api_key
        
        if filters is not None:
            if isinstance(filters, POIFilter):
                filters = filters.dump_dict()
            elif isinstance(filters, dict):
                pass
            else:
                raise ValueError("filters parameter must be dict or POIFilter")
                
        geometry2geojson = self.as_geojson(geometry)
        
        self.parameters = {
            "request": request if request is not None else POIRequestType.POIS,
            "geometry": {
                "buffer": 100,
                "bbox": [
                    geometry2geojson["coordinates"],
                    [round(g - 0.02, 4) for g in geometry2geojson["coordinates"]]
                ],
                "geojson": geometry2geojson
            },
            "filters": filters,
            "limit": 100
        }
        """
        self.parameters = {
            "request": request if request is not None else POIRequestType.POIS,
            "geometry": {
                "buffer": 100,
                "geojson": geometry2geojson
            },
            "filters": filters,
            "limit": 100
        }
        """
        
    def build_url(self):
        url = "https://api.openrouteservice.org/pois?api_key={}".format(self.api_key)
        for key, value in self.parameters.items():
            url += "&" + str(key) + "=" + str(value)
        return url

    def build_json(self):
        return self.parameters

    def as_geojson(self, g):
        if not isinstance(g, list):
            raise ValueError("geometry parameter is not a list")
        geojson_obj = {}
        # g is point
        if isinstance(g[0], float) and isinstance(g[1], float) and len(g) == 2:
            geojson_obj["type"] = "Point"
            geojson_obj["coordinates"] = g
        # g is polyline
        elif isinstance(g[0], list) and len(g) > 1:
            geojson_obj["type"] = "LineString"
            geojson_obj["coordinates"] = [_g for _g in g]
        else:
            raise ValueError("geometry parameter is malformed; cannot process")

        return geojson_obj
            

class POIRequestType(object):
    POIS = "pois"
    STATISTICS = "stats"
    LIST = "list"


class POIFilter(object): 
    def __init__(self):
        self.wheelchair = None
        self.smoking = None
        self.fee = None
        self.name = None

    def __setattr__(self, key, value):
        key = key.lower()
        if key == "wheelchair":
            if value in ["yes", "no", "limited", "designated"]:
                self.__dict__["wheelchair"] = value
        elif key == "smoking":
            if value in ["dedicated", "yes", "no", "separated", "isolated", "outside"]:
                self.__dict__["smoking"] = value
        elif key == "fee":
            if value in ["yes", "no"]:
                self.__dict__["fee"] = value
        elif key == "name":
            self.__dict__["name"] = value
        else:
            self.__dict__[key] = value
            
    def dump_dict(self):
        return {key: [value] for key, value in self.__dict__.items() if value is not None and not key.startswith("__")}
    
