from rdflib import Graph, URIRef, RDFS, SKOS, SDO, Literal
from rdflib.query import Result

from typing import Optional

from config import institute_resource_namespace, institute_ontology_namespace, institute_kg_file_name, \
    institute_resource_prefix, institute_ontology_prefix
from model.resource import Resource
from model.triple import (
    Triple,
    Value,
    ValueDatatype,
)

from institute_kg.settings import BASE_DIR

PREFIX = institute_resource_prefix
PREFIX_ONTOLOGY = institute_ontology_prefix


class RDFConnector:
    def __init__(self):
        self.g = Graph()
        self.property_labels = dict()
        self.init_graph()

    def init_graph(self):
        self.g.parse(str(BASE_DIR) + "/../kgcreation/data/" + institute_kg_file_name)
        self.load_property_labels()

    def run_query(self, query_str: str) -> Result:
        return self.g.query(query_str)

    def get_resource(
        self, resource: Resource, resource_name: str
    ) -> Optional[Resource]:
        print(resource.uri)
        if (URIRef(resource.uri), None, None) not in self.g:
            print(f"{resource.uri} not in graph")
            return

        for _s, p, o in self.g.triples((URIRef(resource.uri), None, None)):
            property_resource = Resource(p)
            property_resource.pref_label = (
                self.property_labels[p] if p in self.property_labels else str(p)
            )

            if p == SKOS.prefLabel:
                resource.pref_label = str(o)
            elif p == RDFS.label and not resource.pref_label:
                resource.pref_label = str(o)

            datatype = ValueDatatype.OTHER
            if p == SDO.image:
                datatype = ValueDatatype.IMAGE
            elif type(o) != Literal:
                datatype = ValueDatatype.URI

            # set object resource
            o_resource = Resource(str(o))
            # set pref_label of object
            for _s1, _p1, o1 in self.g.triples((o, RDFS.label, None)):
                o_resource.pref_label = str(o1)

            value = Value(value=o_resource, datatype=datatype)
            resource.triples.append(Triple(property_resource, value))

        for s, p, o in self.g.triples((None, None, URIRef(resource.uri))):
            property_resource = Resource(p)
            property_resource.pref_label = (
                self.property_labels[p] if p in self.property_labels else str(p)
            )

            if p == SKOS.prefLabel:
                resource.pref_label = str(o)
            elif p == RDFS.label and not resource.pref_label:
                resource.pref_label = str(o)

            # set subject resource
            s_resource = Resource(str(s))
            # set pref_label of subject
            for _s1, _p1, o1 in self.g.triples((s, RDFS.label, None)):
                s_resource.pref_label = str(o1)

            datatype = ValueDatatype.URI
            value = Value(value=s_resource, datatype=datatype)
            resource.object_triples.append(Triple(property_resource, value))

        if not resource.pref_label:
            resource.pref_label = resource_name

        return resource

    def get_ontology_resource_by_name(self, resource_name: str) -> Optional[Resource]:
        resource = Resource(PREFIX_ONTOLOGY + resource_name)
        return self.get_resource(resource, resource_name)

    def get_resource_by_name(self, resource_name: str) -> Optional[Resource]:
        resource = Resource(PREFIX + resource_name)
        return self.get_resource(resource, resource_name)

    def load_property_labels(self) -> None:
        property_label_query = """
        SELECT ?property ?label WHERE {
            ?property a rdf:Property .
            ?property rdfs:label ?label .
        }        
        """
        for res in self.run_query(property_label_query):
            self.property_labels[res.property] = res.label

    def get_property_label(self, property_uri):
        return self.property_labels[property_uri]

    def search(self, query: str) -> Result:
        # get uri, label and list of types of the resource
        search_query = f"""
        SELECT DISTINCT ?uri ?label (GROUP_CONCAT(?type; SEPARATOR=";") AS ?types) WHERE {{
            ?uri rdfs:label ?label .
            ?uri a ?type .
            FILTER regex(?label, "{query}", "i") .
        }}
        GROUP BY ?uri ?label
        """


        print(search_query)
        return self.run_query(search_query)


rdf_connector = RDFConnector()
