# takes the .ttl graph and creates a new .ttl file only with class and property definitions

from rdflib import Graph, RDF, OWL


from config import institute_kg_file_name, institute_resource_namespace, institute_ontology_namespace
from kgcreation.rdf.InstO import InstO
from kgcreation.rdf.InstR import InstR


def extract_schema(input_file: str, output_file: str):
    # Load the original graph from the Turtle file
    g = Graph()
    g.parse(input_file, format="turtle")


    # Create a new graph to store schema-related triples
    schema_graph = Graph()
    schema_graph.bind(institute_ontology_namespace, InstO)
    schema_graph.bind(institute_resource_namespace, InstR)

    # Iterate through triples and filter class and property definitions
    for subj, pred, obj in g:
        if obj in (OWL.Class, RDF.Property):
            schema_graph.add((subj, pred, obj))
            # Also include other relevant properties (like rdfs:label)
            for s, p, o in g.triples((subj, None, None)):
                schema_graph.add((s, p, o))

    # Serialize the new graph to a Turtle file
    schema_graph.serialize(destination=output_file, format="turtle")
    print(f"Schema saved to {output_file}")


# Example usage
extract_schema("../data/" + institute_kg_file_name, "../data/schema.ttl")
