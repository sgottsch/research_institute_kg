class Project:
    def __init__(self, identifier: str, name: str, members=None):
        self.identifier = identifier
        self.name = name
        if not members:
            self.members = []
        else:
            self.members = members

    def print(self):
        print(self.identifier, "->", self.name)
