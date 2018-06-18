from dino_backend.dino.api.meta.feeder import Feeder
from dino_backend.dino.api.wrappers.openrouteservice.bindings import OpenRouteServiceAPIWrapper
from dino_backend.dino.api.wrappers.openrouteservice.route import Profiles, Units, Preferences, Languages

if __name__ == "__main__":
    api = OpenRouteServiceAPIWrapper()
    r = api.get_route(
        waypoints=[[6.7944, 51.2198], [6.761680,51.217942]],
        profile=Profiles.FOOT_WALKING,
        units=Units.METERS,
        preference=Preferences.RECOMMENDED,
        language=Languages.GERMAN,
    )

    f = Feeder()
    f.feed_route(json=r)
    print(f.data_container.get('distance'))
    print(f.data_container.get('duration'))
    print(f.data_container.get('polyline'))
