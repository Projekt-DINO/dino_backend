import uuid


class ID():

    @classmethod
    def generate_id(self):
        return uuid.uuid4()