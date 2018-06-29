import asyncio
import aiohttp
import json

from dino.api.wrappers.openrouteservice.route import *
from dino.api.wrappers.openrouteservice.geocoding import *
from dino.api.wrappers.openrouteservice.pois import *
from dino.api.wrappers.openrouteservice.config import APIConfig
from dino.api.wrappers.openrouteservice.longlat import Waypoint


"""
Class with methods that make use of the APIs at https://openrouteservice.org/documentation/

Requires an API-Key to be set in settings.cfg
"""


class OpenRouteServiceAPIWrapper(object):

    def __init__(self):
        self.config = APIConfig()
        self.async_loop = asyncio.get_event_loop()

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
    def get_route(self, waypoints, profile: str, preference: str, units: str, language: str):
        if isinstance(waypoints, list):
            waypoints = Waypoint.piped(waypoints)

        dct = {
            "coordinates": waypoints,
            "profile": profile,
            "preference": preference,
            "units": units,
            "language": language
        }
        
        direction = Route(api_key=self.config.api_key, **dct)
        url = direction.build_url()
        response = self.async_loop.run_until_complete(self.__send_request(url))
            
        #print('\n'.join([','.join([str(coord) for coord in latlong]) for latlong in response["features"][0]["geometry"]["coordinates"]]))
        print(url)
        print(response)
        return response

    def geocode_reverse_search(self, coords):
        g_search_reverse = GeocodeSearchReverse(api_key=self.config.api_key, coords=coords)
        url = g_search_reverse.build_url()
        response = self.async_loop.run_until_complete(self.__send_request(url, method="GET"))
        print(url)
        print(response)
        return response

    def geocode_search(self, term, coords=None):
        g_search = GeocodeSearch(api_key=self.config.api_key, term=term, coords=coords)
        url = g_search.build_url()
        response = self.async_loop.run_until_complete(self.__send_request(url, method="GET"))
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
    api = OpenRouteServiceAPIWrapper()

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
    api.geocode_search("Rheinturm", [6.761680,51.217942])
