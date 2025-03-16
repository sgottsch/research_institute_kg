import dataclasses
from datetime import date
from typing import List, Set, Dict

from kgcreation.models.city import City
from kgcreation.models.paper import Paper


@dataclasses.dataclass
class Person:
    identifier: str = None
    name: str = None
    phone_number: str = None
    email: str = None
    img: str = None
    identifiers: Dict = dataclasses.field(default_factory=dict)
    date_of_birth: date = None
    positions: List[str] = dataclasses.field(default_factory=list)

    cities: Set[City] = dataclasses.field(default_factory=set)
    institute_kg_uri: str = None
    interests: Set[str] = dataclasses.field(default_factory=set)
    languages: Set[str] = dataclasses.field(default_factory=set)
    buildings: Set[str] = dataclasses.field(default_factory=set)

    google_scholar_id: str = None
    orcid: str = None
    starting_date: date = None

    papers: List[Paper] = dataclasses.field(default_factory=list)

    def __str__(self):
        return f"<Person>: {self.identifier}, {self.name}"
