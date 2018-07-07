from dino_backend.dino.api.meta.core.standards.entity_objects import *
#from dino_backend.dino.database.dynamoDB.put_table_content import putIntoRoutes


class DynamoFeeder(object):

    @staticmethod
    def insert_route(json_container):
        if json_container.get_entity_type() == DinoRoute.__str__():
            json_container.replace_empty_values("null")
            # putIntoRoutes(self.data_container.serialize())

    @staticmethod
    def insert_poi(json_container):
        if json_container.get_entity_type() == PointOfInterest.__str__():
            json_container.replace_empty_values("null")
            # putIntoRoutes(self.data_container.serialize())

