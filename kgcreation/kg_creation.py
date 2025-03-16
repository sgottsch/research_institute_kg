from typing import List

from rdflib import Graph, URIRef, SDO, RDF, RDFS, Literal, OWL, XSD

from config import institute_starting_date_property_label, institute_resource_namespace, institute_ontology_namespace, \
    institute_kg_file_name, institute_super_position
from kgcreation.extractors.institute_website_parser import get_all_persons_from_institute_website
from kgcreation.extractors.wikidata_extractor import get_all_persons_from_wikidata
from kgcreation.extractors.city_index import city_index
from kgcreation.extractors.google_forms_extractor import (
    get_all_persons_from_google_forms,
)
from kgcreation.extractors.google_scholar_extractor import (
    get_all_persons_from_scholar,
)
from kgcreation.extractors.conference_index import conference_index
from kgcreation.extractors.journal_index import journal_index
from kgcreation.extractors.paper_index import paper_index
from kgcreation.extractors.person_index import Identifier
from kgcreation.rdf.InstO import InstO
from kgcreation.rdf.InstR import InstR

from kgcreation.models.person import Person

property_labels = {
    RDFS.subClassOf: "sub class of",
    InstO.coAuthor: "co author",
    InstO.startingDate: institute_starting_date_property_label,
}


def match_persons(*person_lists: List[Person]) -> List[Person]:
    matched_persons = []

    # we rely on the correctness of the person index

    for person_list in person_lists:
        for person in person_list:
            matched_persons.append(person)

    return matched_persons


def create_kg() -> Graph:
    persons_institute_website = get_all_persons_from_institute_website()
    persons_wikidata = get_all_persons_from_wikidata()
    persons_google_forms = get_all_persons_from_google_forms()
    persons_scholar = get_all_persons_from_scholar()

    matched_persons = match_persons(
        persons_institute_website, persons_wikidata, persons_google_forms, persons_scholar
    )

    return create_kg_from_persons(matched_persons)


def urify(resource_str: str) -> str:
    resource_uri_str = resource_str.title().strip().replace(" ", "_")
    # resource_uri_str = from_n3(resource_uri_str.encode('unicode_escape').decode('unicode_escape'))

    return resource_uri_str


def create_kg_from_persons(persons: List[Person]) -> Graph:
    positions = {}

    g = Graph()

    building_dict = {}
    interest_dict = {}
    languages = {}

    # add super class of Institute Positions
    super_position_uri = URIRef(InstO.InstituteAssociate)
    g.add((super_position_uri, RDF.type, OWL.Class))
    g.add((super_position_uri, RDFS.label, Literal(institute_super_position, datatype=XSD.string)))

    # add research field class to the KG
    g.add((URIRef(InstO.ResearchField), RDF.type, OWL.Class))
    g.add((URIRef(InstO.ResearchField), RDFS.label, Literal("Research field", datatype=XSD.string)))

    g.bind(institute_resource_namespace, InstR)
    g.bind(institute_ontology_namespace, InstO)
    g.bind("wd", "https://www.wikidata.org/entity/")

    co_authorships = []
    co_authorship_strings = set()

    for conference in conference_index.get_conferences():
        conference_uri = URIRef(InstR["Conference_" + str(urify(conference.name))])
        conference.institute_kg_uri = conference_uri
        g.add((conference_uri, RDF.type, SDO.Event))
        g.add(
            (conference_uri, RDFS.label, Literal(conference.name, datatype=XSD.string))
        )

    for journal in journal_index.get_journals():
        journal_uri = URIRef(InstR["Journal_" + str(urify(journal.name))])
        journal.institute_kg_uri = journal_uri
        g.add((journal_uri, RDF.type, SDO.Periodical))
        g.add((journal_uri, RDFS.label, Literal(journal.name, datatype=XSD.string)))

    for paper_id, paper in enumerate(paper_index.get_papers()):
        paper_uri = URIRef(InstR["Paper" + str(paper_id)])
        g.add((paper_uri, RDF.type, SDO.ScholarlyArticle))
        g.add((paper_uri, RDFS.label, Literal(paper.title, datatype=XSD.string)))
        # TODO: add year

        if paper.citation:
            g.add(
                (paper_uri, SDO.citation, Literal(paper.citation, datatype=XSD.string))
            )
        if paper.conference:
            g.add((paper_uri, SDO.subjectOf, paper.conference.institute_kg_uri))
        if paper.journal:
            g.add((paper_uri, SDO.isPartOf, paper.journal.institute_kg_uri))

        paper.institute_kg_uri = paper_uri

        # find co-author pairs
        if len(paper.authors) > 1:
            for author1 in paper.authors:
                for author2 in paper.authors:
                    if author1 != author2:
                        if author1.name + "-" + author2.name in co_authorships:
                            continue
                        co_authorship_strings.add(author1.name + "-" + author2.name)
                        co_authorship_strings.add(author2.name + "-" + author1.name)
                        co_authorships.append([author1, author2])
    print("co_authorships:", len(co_authorships))

    for city_id, city in enumerate(city_index.get_cities()):
        city_uri = URIRef(InstR["City" + str(city_id)])
        g.add((city_uri, RDF.type, SDO.City))
        g.add((city_uri, RDFS.label, Literal(city.name)))
        city.uri = city_uri
        print(city.identifiers)

    for person in persons:
        if person.identifier:
            person_uri = URIRef(InstR[person.identifier.capitalize()])
        else:
            person_uri = URIRef(InstR[person.name.title().replace(" ", "")])

        person.institute_kg_uri = person_uri

        g.add((person_uri, RDF.type, SDO.Person))

        if person.name:
            g.add((person_uri, RDFS.label, Literal(person.name)))

        if person.phone_number:
            g.add((person_uri, SDO.telephone, Literal(person.phone_number)))
        if person.email:
            g.add((person_uri, SDO.email, Literal(person.email)))
        if person.img:
            g.add((person_uri, SDO.image, Literal(person.img, datatype=XSD.anyURI)))
        if person.google_scholar_id:
            g.add(
                (
                    person_uri,
                    OWL.sameAs,
                    Literal(
                        "https://scholar.google.com/citations?hl=de&user="
                        + person.google_scholar_id,
                        datatype=XSD.anyURI,
                    ),
                )
            )

        # Buildings
        for building in person.buildings:
            building_uri_str = urify(building)
            if building in building_dict:
                building_uri = building_dict[building]
            else:
                building_uri = InstR[building_uri_str]
                g.add((building_uri, RDF.type, SDO.House))
                g.add((building_uri, RDFS.label, Literal(building)))
                building_dict[building] = building_uri
            g.add((person_uri, SDO.workLocation, building_uri))

        # birth date
        if person.date_of_birth:
            g.add(
                (
                    person_uri,
                    SDO.birthDate,
                    Literal(person.date_of_birth, datatype=XSD.date),
                )
            )
        if person.starting_date:
            g.add(
                (
                    person_uri,
                    InstO.startingDate,
                    Literal(person.starting_date, datatype=XSD.date),
                )
            )

        for position in person.positions:
            if position not in positions:
                position_uri = URIRef(InstO[position.title().replace(" ", "")])
                g.add((position_uri, RDF.type, OWL.Class))
                g.add((position_uri, RDFS.label, Literal(position.capitalize())))
                g.add((position_uri, RDFS.subClassOf, super_position_uri))
                positions[position] = position_uri
            g.add((person_uri, RDF.type, positions[position]))

        if person.interests:
            for interest in person.interests:
                interest = interest.title().strip()
                interest_uri_str = urify(interest)
                if interest_uri_str in interest_dict:
                    interest_uri = interest_dict[interest_uri_str]
                else:
                    interest_uri = InstR[interest_uri_str]
                    g.add((interest_uri, RDF.type, InstO.ResearchField))
                    g.add((interest_uri, RDFS.label, Literal(interest)))
                    interest_dict[interest_uri_str] = interest_uri
                g.add((person_uri, InstO.interest, interest_uri))

        if person.languages:
            for language in person.languages:
                if language not in languages:
                    language_uri = URIRef(InstR[language.title().replace(" ", "")])
                    g.add((language_uri, RDF.type, SDO.Language))
                    g.add(
                        (
                            language_uri,
                            RDFS.label,
                            Literal(language, datatype=XSD.string),
                        )
                    )
                    languages[language] = language_uri
                g.add((person_uri, SDO.knowsLanguage, languages[language]))

        for city in person.cities:
            g.add((person_uri, SDO.location, city.uri))

        for source, identifier in person.identifiers.items():
            if source == Identifier.Wikidata:
                g.add(
                    (
                        person_uri,
                        OWL.sameAs,
                        URIRef(Identifier.Wikidata.value + identifier),
                    )
                )
            elif source == Identifier.ORCID:
                g.add((person_uri, InstO.orcidId, Literal(identifier)))

        for paper in person.papers:
            g.add((paper.institute_kg_uri, SDO.author, person.institute_kg_uri))
            if paper.conference:
                g.add((paper.conference.institute_kg_uri, SDO.author, person.institute_kg_uri))
            if paper.journal:
                g.add((paper.journal.institute_kg_uri, SDO.author, person.institute_kg_uri))
            g.add((paper.institute_kg_uri, SDO.author, person.institute_kg_uri))

    for co_authorship in co_authorships:
        g.add((co_authorship[0].institute_kg_uri, InstO.coAuthor, co_authorship[1].institute_kg_uri))
        g.add((co_authorship[1].institute_kg_uri, InstO.coAuthor, co_authorship[0].institute_kg_uri))

    # add properties
    property_query = "SELECT DISTINCT ?property WHERE { ?a ?property ?b }"
    for res in g.query(property_query):
        rdf_property = res["property"]
        g.add((rdf_property, RDF.type, RDF.Property))
        if rdf_property in property_labels:
            property_label = property_labels[rdf_property]
        else:
            property_label = str(rdf_property)
            if property_label.rfind("/") > property_label.rfind("#"):
                property_label = str(rdf_property).rsplit("/", 1)[-1]
            else:
                property_label = str(rdf_property).rsplit("#", 1)[-1]

        g.add((rdf_property, RDFS.label, Literal(property_label)))

    # add property labels
    class_label_dict = {
        SDO.ScholarlyArticle: "ScholarlyArticle",
        SDO.Event: "Event",
        SDO.Periodical: "Periodical",
        SDO.City: "City",
        SDO.Language: "Language",
        SDO.House: "House"
    }

    for rdf_class, class_label in class_label_dict.items():
        g.add((rdf_class, RDF.type, OWL.Class))
        g.add((rdf_class, RDFS.label, Literal(class_label)))

    return g


if __name__ == "__main__":
    g = create_kg()
    g.serialize("kgcreation/data/" + institute_kg_file_name)
    print("Created KG")
