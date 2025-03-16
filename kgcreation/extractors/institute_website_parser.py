from typing import List, TYPE_CHECKING

import requests
from bs4 import BeautifulSoup

from kgcreation.extractors.person_index import person_index, Identifier

from kgcreation.models.person import Person
from kgcreation.rdf.InstO import InstO

# This is an example script that needs to be adapted to the institute's website

def get_persons(url: str) -> List[Person]:
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")

    persons = []

    for div in soup.select("..."):
        inst_identifier = "..."
        name = "..."
        email = "..."
        positions = {InstO.Researcher, InstO.PhDStudent} # Example

        person = person_index.get_person_by_id_or_name(
            Identifier.INST, inst_identifier, name
        )
        person.email = email
        person.positions = positions

        persons.append(person)

    return persons


def get_all_persons_from_institute_website() -> List[Person]:
    persons = []
    # persons.extend(get_persons("...")) # TODO: un-comment when ready

    return persons

