from dataclasses import dataclass, field


@dataclass
class Resource:
    uri: str
    triples: list = field(default_factory=list)
    pref_label: str = None
    object_triples: list = field(default_factory=list)

    def __str__(self):
        return self.pref_label if self.pref_label else self.uri
