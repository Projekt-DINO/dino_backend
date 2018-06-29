from dino_backend.dino.api.wrappers.openrouteservice.longlat import Waypoint


class GeocodeSearch(object):

    def __init__(self, api_key, term, coords=None):
        self.result_size = 10
        self.country = "DEU"
        self.api_key = api_key
        self.parameters = {
            "text": str(term),
        }
        if coords is not None:
            if not isinstance(coords, Waypoint):
                raise ValueError("Coords must be instance of Waypoint, got {}".format(type(coords)))
            self.parameters["focus.point.lon"] = coords.longitude
            self.parameters["focus.point.lat"] = coords.latitude


    def build_url(self):
        url = "https://api.openrouteservice.org/geocode/search?api_key={}&size={}&boundary.country={}".format(self.api_key, self.result_size, self.country)
        for key, value in self.parameters.items():
            url += "&" + str(key) + "=" + str(value)
        return url


class GeocodeSearchReverse(object):
    def __init__(self, api_key, coords):
        self.result_size = 10
        self.country = "DEU"
        self.api_key = api_key

        if not isinstance(coords, Waypoint):
            raise ValueError("Coords must be Waypoint or List, got {}".format(type(coords)))

        self.parameters = {
            "point.lon": coords.longitude,
            "point.lat": coords.latitude,
        }

    def build_url(self):
        url = "https://api.openrouteservice.org/geocode/reverse?api_key={}&size={}&boundary.country={}".format(self.api_key, self.result_size, self.country)
        for key, value in self.parameters.items():
            url += "&" + str(key) + "=" + str(value)
        return url
