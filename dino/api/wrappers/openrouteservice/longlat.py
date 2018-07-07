
"""
A Waypoint is essentially a pair of a longitude and a latitde value.

This class helps to standardize longlat pairs, as well as providing
other methods which may be important for use in the backend.
"""
class Waypoint(object):

    def __init__(self, longitude, latitude):
        self.longitude = self.__rounded(longitude)
        self.latitude = self.__rounded(latitude)

    def __str__(self):
        return "[{}, {}]".format(self.longitude, self.latitude)

    """
    Called when self.attr = value is used.
    
    If longitude or latitude are being set, this modified __setattr__
    makes sure the new values are not out of bounds and are rounded
    to the correct amount of floating points.
    
    If they are not inbounds, an error will be thrown.
    """
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

    """
    Called like Waypoint.piped([Waypoint1, Waypoint2, Waypoint3])
    
    Takes a list of Waypoint objects and joins them into a pipe separated string.
    
    Return example: "32.402522,92.452452|20.556242,54.553623|35.636242,60.258315"
    """
    @classmethod
    def piped(cls, waypoints):
        _piped = ""
        for wp in waypoints:
            if not isinstance(wp, cls):
                raise ValueError("{} is not Waypoint object.")
            _piped += wp.comma_separated() + "|"
        _piped = _piped[:len(_piped)-1]  # cut off dangling |
        return _piped

    """
    Transforms the Waypoint object into a longlat string.
    
    Return example: "232.402542,92.452453"
    """
    def comma_separated(self):
        return "{},{}".format(self.longitude, self.latitude)

    """
    Returns the longlat values in an list.
    """
    def aslist(self):
        return [self.longitude, self.latitude]

    """
    Returns the longlat values in a dictionary.
    """
    def asdict(self):
        return {"longitude": self.longitude, "latitude": self.latitude}

    """
    Round a floating number to number with 6 floating points.
    
    This is used to standardize the size of every longitude and latitude coordinate this
    class ever touches.
    """
    def __rounded(self, coord):
        return round(coord, 6)

    """
    Checks if a latitude value is inbounds.
    """
    def __latitude_is_inbounds(self, value):
        northbound = 80.0
        southbound = -80.0
        return northbound >= value >= southbound

    """
    Checks if a longitude value is inbounds.
    """
    def __longitude_is_inbounds(self, value):
        westbound = 180.0
        eastbound = -180.0
        return westbound >= value >= eastbound
