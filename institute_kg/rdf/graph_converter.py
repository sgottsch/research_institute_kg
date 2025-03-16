from typing import Dict, List, Optional, Iterable

from config import institute_ontology_namespace, positions_map
from kgcreation.rdf.InstO import InstO
from rdf.rdf_connector import rdf_connector
from rdflib import RDF, SDO, RDFS, OWL
from rdflib.term import URIRef

with_papers = False

type_map = {
    SDO.Person: "Person",
    SDO.City: "City",
    SDO.House: "House",
    SDO.ScholarlyArticle: "Paper",
    SDO.Language: "Language",
    InstO.ResearchField: "ResearchField"
}
type_map |= positions_map


def convert_to_json(
    g,
    type_filter: Optional[Iterable[URIRef]] = None,
    property_filter: str = "?p",
    delete_unconnected_nodes: bool = False,
) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    ignored_classes = {SDO.ScholarlyArticle} if not type_filter else set()
    nodes = []
    node_index = {}
    edges = []

    json_graph = {"elements": {"nodes": nodes, "edges": edges}}
    rdf_classes = set()
    for s, p, o in g.triples((None, RDF.type, OWL.Class)):
        rdf_classes.add(s)

    # only keep interests that exist more than once
    single_interests = set()
    single_interests_query = """
        SELECT ?interest WHERE {
            ?person @institute_ontology_namespace@:interest ?interest
        } GROUP BY ?interest
        HAVING (COUNT(?person) = 1)
    """
    single_interests_query = single_interests_query.replace("@institute_ontology_namespace@", institute_ontology_namespace)
    for res in rdf_connector.run_query(single_interests_query):
        single_interests.add(res["interest"])

    for s, p, o in g.triples((None, RDF.type, None)):
        if o == RDF.Property:
            continue
        if s in rdf_classes:
            continue
        if o in ignored_classes:
            continue

        if s in single_interests:
            continue

        if type_filter and o not in type_filter:
            continue

        if s not in node_index:
            node_id = "node" + str(len(nodes))
            node_obj = {"data": {"id": node_id, "uri": str(s)}, "classes": ""}
            node_index[s] = node_obj
            nodes.append(node_obj)
        else:
            node_obj = node_index[s]

        if o in type_map:
            node_obj["classes"] += type_map[o] + " "

    for s, p, o in g.triples((None, RDFS.label, None)):
        if s not in node_index:
            continue
        node_obj = node_index[s]
        node_obj["data"]["label"] = str(o)
        node_obj["data"]["label"] = str(o)

    triple_query = "SELECT ?s ?p ?o WHERE {"
    if property_filter == "?p":
        triple_query += (
            "?s ?p ?o ." "FILTER(?p != rdf:type) ." "FILTER(?p != rdfs:subClassOf ) ."
        )
    else:
        triple_query += (
            f"?s <{property_filter}> ?o . BIND (<{property_filter}> AS ?p) ."
        )
    triple_query += "FILTER(!isLiteral(?o)) ."
    triple_query += "FILTER NOT EXISTS { ?s a rdf:Property } .}"

    connected_nodes = set()

    for res in rdf_connector.run_query(triple_query):
        if res["s"] in node_index and res["o"] in node_index:
            edge_label = rdf_connector.get_property_label(res["p"])
            source_node_id = node_index[res["s"]]["data"]["id"]
            target_node_id = node_index[res["o"]]["data"]["id"]
            edge_obj = {
                "data": {
                    "label": edge_label,
                    "source": source_node_id,
                    "target": target_node_id,
                }
            }
            edges.append(edge_obj)
            connected_nodes.add(source_node_id)
            connected_nodes.add(target_node_id)

    # delete unconnected nodes
    if delete_unconnected_nodes:
        print("DELETE")
        json_graph["elements"]["nodes"] = [node for node in json_graph["elements"]["nodes"] if node["data"]["id"] in connected_nodes]

    # TODO: For efficiency, with SPARQL query that takes only non-literal triples?
    # for s, p, o in g.triples((None, None, None)):
    #    if s in node_index and o in node_index:
    #        edge_label = rdf_connector.get_property_label(p)
    #        edge_obj = { "data": {"label": edge_label, "source": node_index[s]["data"]["id"], "target": node_index[o]["data"]["id"]} }
    #        edges.append(edge_obj)

    return json_graph
