class Waypoint(object):

    def __init__(self, longitude, latitude):
        self.longitude = self.__rounded(longitude)
        self.latitude = self.__rounded(latitude)

    def __setattr__(self, attr, value):
        if attr == "longitude":
            if not self.__longitude_is_inbounds(value):
                raise ValueError("Longitude is out of bounds; value must be in range {180, -180}")
            self.__dict__["longitude"] = self.__rounded(value)
        elif attr == "latitude":
            if not self.__latitude_is_inbounds(value):
                raise ValueError("Latitude is out of bounds; value must be in range {80, -80}")
            self.__dict__["latitude"] = self.__rounded(value)
        else:
            if attr not in self.__dict__:
                raise ValueError("Attempt to set value of unknown attribute {}".format(attr))
            self.__dict__[attr] = value

    @classmethod
    def piped(cls, waypoints):
        _piped = ""
        for wp in waypoints:
            if not isinstance(wp, cls):
                raise ValueError("{} is not Waypoint object.")
            _piped += wp.comma_separated() + "|"
        _piped = _piped[:len(_piped)-1]  # cut off dangling |
        return _piped

    def comma_separated(self):
        return "{},{}".format(self.longitude, self.latitude)

    def asarray(self):
        return [self.longitude, self.latitude]

    def asdict(self):
        return {"longitude": self.longitude, "latitude": self.latitude}

    def __rounded(self, coord):
        return round(coord, 6)

    def __latitude_is_inbounds(self, value):
        northbound = 80.0
        southbound = -80.0
        return northbound >= value >= southbound

    def __longitude_is_inbounds(self, value):
        westbound = 180.0
        eastbound = -180.0
        return westbound >= value >= eastbound
