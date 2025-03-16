import dataclasses
from typing import List, TYPE_CHECKING

from kgcreation.models.conference import Conference
from kgcreation.models.journal import Journal

if TYPE_CHECKING:
    from kgcreation.models.person import Person


@dataclasses.dataclass
class Paper:
    title: str = None
    citation: str = None
    conference: Conference = None
    journal: Journal = None
    institute_kg_uri: str = None
    authors: List["Person"] = dataclasses.field(default_factory=list)

    def __str__(self):
        return f"<Paper>: {self.title}"
