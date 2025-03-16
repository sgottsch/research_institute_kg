from typing import Iterable, Dict, Set

from config import city_matches
from kgcreation.models.city import City


def unify_name(name: str) -> str:
    name = name.replace("  ", " ")
    name = name.replace(",", "")
    name = name.strip()
    return name


class CityIndex:
    def __init__(self):
        self.citys_by_identifier: Dict[str, City] = {}
        self.citys_by_name: Dict[str, City] = {}
        self.cities: Set[City] = set()

    def get_cities(self) -> Iterable[City]:
        return self.citys_by_identifier.values()

    def get_city_by_id_or_name(self, identifier, name: str) -> City:
        identifier = identifier.replace(".m.wikipedia.org", ".wikipedia.org")

        identifiers = set()
        identifiers.add(identifier)

        if identifier in city_matches:
            identifiers.add(city_matches[identifier])

        if name:
            name = unify_name(name)
        city = None

        # get city by ID
        for identifier in identifiers:
            if identifier in self.citys_by_identifier:
                city = self.citys_by_identifier[identifier]

                # update city name
                if not city.name and name:
                    city.name = name
                    self.citys_by_name[name] = city

        # find city by name
        if not city and name and name in self.citys_by_name:
            city = self.citys_by_name[name]

            # update ID
            if identifier:
                print("CI", city.identifiers)
                city.identifiers.add(identifier)
                self.citys_by_identifier[identifier] = city

        # create new city
        if not city:
            city = City()
            city.name = name
            if identifier:
                city.identifiers.add(identifier)
                self.citys_by_identifier[identifier] = city
            if name:
                city.name = name
                self.citys_by_name[name] = city

        self.cities.add(city)
        return city


city_index = CityIndex()
