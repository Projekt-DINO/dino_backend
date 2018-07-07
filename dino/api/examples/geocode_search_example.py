from dino_backend.dino.api.wrappers.openrouteservice.bindings import ORSWrapper
from dino_backend.dino.api.wrappers.openrouteservice.longlat import Waypoint
from dino_backend.dino.api.meta.core.container import JSONContainer


if __name__ == "__main__":
    api = ORSWrapper()
    poi_results = api.geocode_search(term="Kö")
    data_container = JSONContainer.make_poi_container(json=poi_results)

    data_container.replace_empty_values("null")
    print(data_container.as_json())
    print(data_container)
    print(data_container.get("coordinates"))
    print(type(data_container))
    print(type(data_container.serialize()))
    print(data_container.as_standardized_json())
