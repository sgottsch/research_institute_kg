from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef

class InstO(DefinedNamespace):
    """
    InstO Namespace Vocabulary Terms
    """

    _fail = False

    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    Project: URIRef
    orcidId: URIRef
    scholarId: URIRef
    coAuthor: URIRef
    startingDate: URIRef
    ResearchField: URIRef
    interest: URIRef
    ResearchGroupLeader: URIRef
    PhDStudent: URIRef
    Administration: URIRef
    InstituteAssociate: URIRef
    # Extend with more if needed


    _NS = Namespace("https://l3skg.l3s.uni-hannover.de/ontology/")
