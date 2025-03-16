from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef

from config import institute_resource_prefix


class InstR(DefinedNamespace):
    """
    InstR Namespace Vocabulary Terms
    """

    _fail = False
    _warn = False

    _NS = Namespace(institute_resource_prefix)
