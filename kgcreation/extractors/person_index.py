from enum import Enum
from typing import Dict

from config import person_name_parts_to_remove, institute_resource_prefix
from kgcreation.models.person import Person


class Identifier(Enum):
    Wikidata = "https://www.wikidata.org/entity/"
    ORCID = "http://orcid.org/"
    SCHOLAR = "https://scholar.google.com/citations?user="
    INST = institute_resource_prefix


def unify_name(name: str) -> str:

    for item in person_name_parts_to_remove:
        name = name.replace(item, "")

    name = name.replace("  ", " ").strip().title()
    return name

class PersonIndex:
    def __init__(self):
        self.persons_by_identifier: Dict[Identifier, Dict[str, Person]] = {
            source: {} for source in Identifier
        }
        self.persons_by_name = {}

    def get_person_by_id_or_name(
        self, source: Identifier, identifier: str, name: str
    ) -> Person:
        if name:
            name = unify_name(name)
        person = None

        # get person by ID
        if identifier and identifier in self.persons_by_identifier[source]:
            person = self.persons_by_identifier[source][identifier]

            # update person name
            if not person.name and name:
                person.name = name
                self.persons_by_name[name] = person

        # find person by name
        elif name and name in self.persons_by_name:
            person = self.persons_by_name[name]

            # update ID
            if identifier:
                person.identifiers[source] = identifier
                self.persons_by_identifier[source][identifier] = person

        # create new person
        if not person:
            person = Person()
            if identifier:
                person.identifiers[source] = identifier
                self.persons_by_identifier[source][identifier] = person
            if name:
                person.name = name
                self.persons_by_name[name] = person

        return person


person_index = PersonIndex()
