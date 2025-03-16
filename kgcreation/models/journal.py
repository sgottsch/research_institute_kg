class Journal:

    def __init__(self, name: str = None):
        self.name = name
        self.institute_kg_uri = None

    def print(self):
        print(self.name)