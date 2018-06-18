
class GeocodeSearch(object):

    def __init__(self, api_key, term, coords=None):
        self.result_size = 10
        self.country = "DEU"
        self.api_key = api_key
        self.parameters = {
            "text": str(term),
        }
        if coords is not None:
            self.parameters["focus.point.lon"] = coords[0]
            self.parameters["focus.point.lat"] = coords[1]

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
        self.parameters = {
            "point.lon": coords[0],
            "point.lat": coords[1],
        }

    def build_url(self):
        url = "https://api.openrouteservice.org/geocode/reverse?api_key={}&size={}&boundary.country={}".format(self.api_key, self.result_size, self.country)
        for key, value in self.parameters.items():
            url += "&" + str(key) + "=" + str(value)
        return url
