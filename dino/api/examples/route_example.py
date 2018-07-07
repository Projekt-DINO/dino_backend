from dino_backend.dino.api.meta.feeder import DynamoFeeder
from dino_backend.dino.api.wrappers.openrouteservice.bindings import ORSWrapper
from dino_backend.dino.api.wrappers.openrouteservice.route import Profiles, Units, Preferences, Languages
from dino_backend.dino.api.wrappers.openrouteservice.longlat import Waypoint
from dino_backend.dino.api.meta.core.container import JSONContainer


if __name__ == "__main__":
    api = ORSWrapper()
    r = api.get_route(
        start_waypoint=Waypoint(6.7944, 51.2198),  # düsseldorf hbf
        end_waypoint=Waypoint(6.779269, 51.222282),  # kö
        inter_waypoints=[Waypoint(6.761680, 51.217942)],  # rheinturm
        profile=Profiles.FOOT_WALKING,
        units=Units.METERS,
        preference=Preferences.RECOMMENDED,
        language=Languages.GERMAN,
    )
    data_container = JSONContainer.make_api_route_container(json=r)
    data_container.replace_empty_values("null")
    print(data_container.as_json())
    print(data_container)
    print(data_container.get('distance'))
    print(data_container.get('duration'))
    print(data_container.get('polyline'))
    print(type(data_container))
    print(type(data_container.serialize()))
    # print('\n'.join([','.join([str(coord) for coord in latlong]) for latlong in data_container.get("polyline")]))
    print(data_container.as_standardized_json())
