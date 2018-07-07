from dino_backend.dino.api.wrappers.openrouteservice.bindings import ORSWrapper
from dino_backend.dino.api.wrappers.openrouteservice.longlat import Waypoint
from dino_backend.dino.api.wrappers.openrouteservice.route import Profiles, Units, Preferences, Languages
from dino_backend.dino.api.meta.core.container import JSONContainer
from dino_backend.dino.api.meta.core.factory import create_dino_route


if __name__ == "__main__":
    api = ORSWrapper()


    stops = [
        "Hauptbahnhof",
        "Rheinturm",
        "Medienhafen"
    ]

    print(create_dino_route(stops))
    """
    stop_data_containers = []
    for name in stops:
        stop_data_containers.append(JSONContainer.make_poi_container(json=api.geocode_search(term=name)))

    route_container = JSONContainer.make_api_route_container(
        json=api.get_route(
                start_waypoint=Waypoint(stop_data_containers[0].get("coordinates")[0], stop_data_containers[0].get("coordinates")[1]),
                inter_waypoints=[Waypoint(_stop.get("coordinates")[0], _stop.get("coordinates")[1]) for _stop in stop_data_containers[1:len(stop_data_containers)-1]],
                end_waypoint=Waypoint(stop_data_containers[-1].get("coordinates")[0], stop_data_containers[-1].get("coordinates")[1]),
                profile=Profiles.FOOT_WALKING,
                units=Units.METERS,
                language=Languages.GERMAN,
                preference=Preferences.RECOMMENDED,
            )
    )

    # print(route_container.as_json())
    # print('\n'.join([','.join([str(coord) for coord in latlong]) for latlong in route_container.get("polyline")]))
    """


