from dino_backend.dino.api.meta.util import list_type_of
from dino_backend.dino.api.wrappers.openrouteservice.longlat import Waypoint
from dino_backend.dino.api.meta.core.container import JSONContainer
from dino_backend.dino.api.meta.core.standards.entity_objects import PointOfInterest
from dino_backend.dino.api.wrappers.openrouteservice.bindings import ORSWrapper, APIError
from dino_backend.dino.api.wrappers.openrouteservice.route import Profiles, Preferences, Units, Languages


def create_dino_route(pois):
    if not isinstance(pois, list):
        raise ValueError("pois parameter must be list, got {} instead.".format(pois))
    if len(pois) < 2:
        raise ValueError("Must provide at least 2 pois.")

    poi_containers = []
    api = ORSWrapper()

    if list_type_of(pois, str):
        for poi_search_term in pois:
            poi_containers.append(JSONContainer.make_poi_container(json=api.geocode_search(term=poi_search_term)))
    elif list_type_of(pois, Waypoint):
        for poi_waypoint in pois:
            poi_containers.append(JSONContainer.make_poi_container(json=api.geocode_reverse_search(poi_waypoint)))
    elif list_type_of(pois, JSONContainer):
        for container in pois:
            if not container.get_container_entity_type() == PointOfInterest.__str__():
                raise ValueError("pois must be either a list of ONLY JSONContainers, ONLY Strings or ONLY Waypoints.")
        poi_containers = pois
    else:
        raise ValueError("pois must be either a list of ONLY JSONContainers, ONLY Strings or ONLY Waypoints.")

    route_container = JSONContainer.make_api_route_container(
        json=api.get_route(
                start_waypoint=Waypoint(poi_containers[0].get("coordinates")[0], poi_containers[0].get("coordinates")[1]),
                inter_waypoints=[Waypoint(_stop.get("coordinates")[0], _stop.get("coordinates")[1]) for _stop in poi_containers[1:len(poi_containers)-1]],
                end_waypoint=Waypoint(poi_containers[-1].get("coordinates")[0], poi_containers[-1].get("coordinates")[1]),
                profile=Profiles.FOOT_WALKING,
                units=Units.METERS,
                language=Languages.GERMAN,
                preference=Preferences.RECOMMENDED,
            )
    )

    route_container.replace_empty_values("null")
    json_base = {
        "stops": [],
        "route": route_container.as_standardized_json()
    }

    for idx, container in enumerate(poi_containers):
        container.set("checkpoint", idx)
        container.replace_empty_values("null")
        json_base["stops"].append(container.as_standardized_json())

    return json_base
