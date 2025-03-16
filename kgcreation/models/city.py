class City:
    def __init__(self, name: str = None, sameAs_uris=None):
        self.name = name
        if not sameAs_uris:
            self.sameAs_uris = []
        else:
            self.sameAs_uris = sameAs_uris
        self.uri = None
        self.identifiers = set()

    def print(self):
        print(self.identifiers, self.name)
