import asyncio
import aiohttp
import json

from dino_backend.dino.api.wrappers.openrouteservice.route import *
from dino_backend.dino.api.wrappers.openrouteservice.geocoding import *
from dino_backend.dino.api.wrappers.openrouteservice.pois import *
from dino_backend.dino.api.wrappers.openrouteservice.config import APIConfig
from dino_backend.dino.api.wrappers.openrouteservice.longlat import Waypoint


"""
Class with methods that make use of the APIs at https://openrouteservice.org/documentation/

Requires an API-Key to be set in settings.cfg

ORS = OpenRouteService
"""


class ORSWrapper(object):

    def __init__(self):
        self.config = APIConfig()
        self.async_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.async_loop)

    """
    Binding to https://openrouteservice.org/documentation/#/reference/directions/directions/directions-service

    Returns a route between two or more locations for a selected profile
    and its settings as GeoJSON response.

    Arguments: 
        -:: waypoints (str or list) >> Represents the list of waypoints
                                       that should be visited by the
                                       route calculated in the API.

            > A waypoint is represented by two floats, separated by a
              comma.

              !!! IMPORTANT !!!

              The left value of a longlat pair must be the waypoint's
              longitude coordinate and the right value is the waypoint's
              latitude.

            > This parameter should be a list and the program will
              automatically convert the list to the API's wanted
              pipeline format. 
              E.g. [[94.2345, 24.3252], [2.4255, 35.2345]]

            > The API wants a pipeline separated string, which looks
              like the following:
              "94.2345,24.3252|2.4255,35.2345"

            
        -:: profile (str) >> Describes the profile of the route that will
                             be considered while calculating the route.
                            
            > Must be one of:
                Profiles.DRIVING_CAR
                Profiles.DRIVING_HGV
                Profiles.CYCLING_REGULAR
                Profiles.CYCLING_ROAD
                Profiles.CYCLING_SAFE
                Profiles.CYCLING_MOUNTAIN
                Profiles.CYCLING_TOUR
                Profiles.FOOT_WALKING
                Profiles.FOOT_HIKING
                Profiles.WHEELCHAIR


        -:: preference (str) >> Sets the preferred speed of the route
                                when using it.
                               
            > Must be one of:
                Preferences.FASTEST
                Preferences.RECOMMENDED
                Preferences.SHORTEST


        -:: units (str) >> Sets the distance unit used for the route
        
            > Must be one of:
                Units.METERS
                Units.KILOMETERS
                Units.MILES


        -:: language (str) >> By default, the API returns navigation
                              instructions for certain segments of the
                              route created in the API. This value sets
                              the language in which these instructions
                              will be translated to.
                             
            > Must be one of:
                Languages.ENGLISH
                Languages.GERMAN
                Languages.RUSSIAN
                Languages.DANISH
                Languages.SPANISH
                Languages.FRENCH
                Languages.ITALIAN
                Languages.DUTCH
                Languages.CHINESE
                Languages.SWEDISH
                Languages.TURKISH
                Languages.GREEK
                Languages.BRAZILIAN_PORTUGUESE
    """
    def get_route(self, start_waypoint, end_waypoint, profile: str, preference: str, units: str, language: str, inter_waypoints=None):
        if inter_waypoints is not None:
            if not isinstance(inter_waypoints, list):
                raise ValueError("Parameter intermediateWaypoints must be of type list, not {}".format(type(inter_waypoints)))
            wps = [start_waypoint]
            wps += inter_waypoints
            wps.append(end_waypoint)
            waypoints = Waypoint.piped(wps)
        else:
            waypoints = Waypoint.piped([start_waypoint, end_waypoint])

        dct = {
            "coordinates": waypoints,
            "profile": profile,
            "preference": preference,
            "units": units,
            "language": language
        }
        
        direction = Route(api_key=self.config.api_key, **dct)
        url = direction.build_url()
        response = self.async_loop.run_until_complete(self.__send_request(url, method="GET"))
            
        #print('\n'.join([','.join([str(coord) for coord in latlong]) for latlong in response["features"][0]["geometry"]["coordinates"]]))
        print(url)
        print(response)
        return response

    """
    Binding to https://api.openrouteservice.org/geocode/reverse
    
    Returns a list of POIs, streets, etc. near a given Waypoint (a longlat coordinate).
    
    :coords: must be either a list or a Waypoint object
    :return: JSON object (may return a JSON with an error code if something went wrong)
    """
    def geocode_reverse_search(self, coords, ensure_poi=True):
        g_search_reverse = GeocodeSearchReverse(api_key=self.config.api_key, coords=coords)
        url = g_search_reverse.build_url()
        response = self.async_loop.run_until_complete(self.__send_request(url, method="GET"))
        if ensure_poi and "features" in response:
            filtered_features = []
            for feature in response["features"]:
                if feature["properties"]["layer"] == "venue":  # venues usually refer to POIs from what I've seen
                    filtered_features.append(feature)
            response["features"] = filtered_features
            if len(response["features"]) == 0:  # only do this check if we are modifying the features, the ORS API probably never returns something with 0 results by itself and instead throws an error or something
                return {"Error": "No POIs were found on waypoint {}".format(str(coords))}
            elif len(response["features"]) > 1:
                response["features"] = [response["features"][0]]  # usually the first result has the highest confidence value, so return only that instead of a list
        print(url)
        print(response)
        return response

    """
    Binding to https://api.openrouteservice.org/geocode/search
    
    Returns a list of POIs, streets, etc. whose names may be related to a search term.
    
    :term: The search term used to look for POIs (str)
    :ensure_poi: Remove any results that is not a POI (i.e. streets will be removed if this is True)
    :coords: (optional) longlat coordinates as a Waypoint object or a List, which helps to narrow down results to any result which is close to this coordinate
    :return: JSON object (may return a JSON with an error code if something went wrong)
    """
    def geocode_search(self, term, ensure_poi=True, coords=None):
        g_search = GeocodeSearch(api_key=self.config.api_key, term=term, coords=coords)
        url = g_search.build_url()
        response = self.async_loop.run_until_complete(self.__send_request(url, method="GET"))
        if ensure_poi and "features" in response:
            filtered_features = []
            for feature in response["features"]:
                if feature["properties"]["layer"] == "venue":  # venues usually refer to POIs from what I've seen
                    filtered_features.append(feature)
            response["features"] = filtered_features
            if len(response["features"]) == 0:  # only do this check if we are modifying the features, the ORS API probably never returns something with 0 results by itself and instead throws an error or something
                return {"Error": "No POIs were found for search term {}".format(term)}
            elif len(response["features"]) > 1:
                response["features"] = [response["features"][0]]  # usually the first result has the highest confidence value, so return only that instead of a list
        print(url)
        print(response)
        return response

    """
    def get_points_of_interest(self, geometry, filters, request=None):
        poi = PointOfInterest(api_key=self.config.api_key, geometry=geometry, filters=filters, request=request)
        response = self.async_loop.run_until_complete(self.__send_request(url=poi.url, method="POST", json=poi.build_json()))
        # print(url)
        print(response)
        return response
    """
        
    async def __send_request(self, url, method="GET", json=None):
        session = aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0'})
        _json = {}
        try:
            if method == "GET":
                async with session.get(url, json=json) as resp:
                    _json = await resp.json()
                    if resp.status == 200:
                        return _json
                    else:
                        raise APIError("Failed to fetch data from API: {}".format(_json))
            elif method == "POST":
                async with session.post(url, json=json) as resp:
                    _json = await resp.json()
                    if resp.status == 200:
                        return _json
                    else:
                        raise APIError("Failed to fetch data from API: {}".format(_json))
        except Exception as e:
            print(str(e))
        finally:
            await session.close()


class APIError(Exception):
    pass


if __name__ == "__main__":
    api = ORSWrapper()

    """
    api.get_route(
        waypoints=[[6.7944, 51.2198], [6.761680,51.217942]],
        profile=Profiles.FOOT_WALKING,
        units=Units.METERS,
        preference=Preferences.RECOMMENDED,
        language=Languages.GERMAN,
    )
    """

    """
    poi_filter = POIFilter()
    poi_filter.fee = "yes"
    api.get_points_of_interest(geometry=[6.761680,51.217942], filters=poi_filter, request=POIRequestType.POIS)
    """

    # api.geocode_reverse_search([6.761680,51.217942])
    api.geocode_search("Rheinturm", [6.761680, 51.217942])
