from SPARQLWrapper import SPARQLWrapper, JSON

from config import institute_wikidata_id
from kgcreation.models.person import Person
from kgcreation.models.city import City
from kgcreation.extractors.person_index import person_index, Identifier
from kgcreation.extractors.city_index import city_index

sparql_wrapper_wikidata = SPARQLWrapper(
    "https://query.wikidata.org/sparql",
    agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
)
sparql_wrapper_wikidata.setReturnFormat(JSON)


def get_all_persons_from_wikidata():
    persons = []

    query = """
        SELECT ?person ?personLabel ?placeOfBirth ?placeOfBirthLabel
        WHERE 
        {
    
          ?person wdt:P31 wd:Q5.
    
          { ?person wdt:P108 wd:@institute_wikidata_id@ . }
          UNION
          { ?person wdt:P1416 wd:@institute_wikidata_id@ . }
    
          OPTIONAL { ?person wdt:P19 ?placeOfBirth } .
    
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # <span lang="en" dir="ltr" class="mw-content-ltr">Helps get the label in your language, if not, then en language</span>
    }
    """
    query = query.replace("@institute_wikidata_id@", institute_wikidata_id)

    sparql_wrapper_wikidata.setQuery(query)

    for res in sparql_wrapper_wikidata.queryAndConvert()["results"]["bindings"]:
        wikidata_id = str(res["person"]["value"]).rsplit("/", 1)[1]
        person = person_index.get_person_by_id_or_name(
            Identifier.Wikidata, wikidata_id, res["personLabel"]["value"]
        )
        persons.append(person)

        if "placeOfBirth" in res:
            city = city_index.get_city_by_id_or_name(
                res["placeOfBirth"]["value"].rsplit("/", 1)[1],
                name=res["placeOfBirthLabel"]["value"],
            )
            # city = City(identifier=res["placeOfBirth"]["value"].rsplit('/', 1)[1],
            #            name=res["placeOfBirthLabel"]["value"], sameAs_uris=[res["placeOfBirthLabel"]["value"]])
            person.cities.add(city)

    return persons


if __name__ == "__main__":
    persons = get_all_persons_from_wikidata()
    for person in persons:
        print(person.name, person.sameAs_uris)
