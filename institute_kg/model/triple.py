from dataclasses import dataclass
from enum import Enum

from model.resource import Resource


class ValueDatatype(Enum):
    IMAGE = "image"
    URI = "uri"
    OTHER = "other"


@dataclass
class Value:
    value: Resource
    datatype: ValueDatatype


@dataclass
class Triple:
    rdf_property: Resource
    value: Value
