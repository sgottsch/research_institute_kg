import dataclasses
from typing import List, Tuple

from django.urls import reverse
from django.views.generic.edit import FormView

from config import kg_name, institute_name
from rdf.rdf_connector import rdf_connector
from .forms import SearchForm

SITE_SEARCH = "search"


@dataclasses.dataclass
class SearchResult:
    uri: str
    identifier: str
    label: str
    url: str
    types: List[Tuple[str, str]] = None


def search_result(query) -> List[SearchResult]:
    """Get the resource names"""
    results = rdf_connector.search(query)
    res = []
    for r in results:
        identifier = r.uri.split("/")[-1]
        types = []
        for type in r.types.split(";"):
            type_name = type.split("/")[-1]
            type_url = type
            if type.split("/")[-2] in ("resource", "ontology"):
                # internal links
                type_url = reverse(type.split("/")[-2], args=[type_name])
            types.append((type_name, type_url))
        url = "uri"
        if r.uri.split("/")[-2] in ("resource", "ontology"):
            # internal links
            url = reverse(r.uri.split("/")[-2], args=[identifier])
        res.append(SearchResult(url, identifier, r.label, url, types))
    return res


class SearchView(FormView):
    template_name = "search/index.html"
    form_class = SearchForm

    def form_valid(self, form):
        results = search_result(form.data["query"])
        return self.render_to_response(self.get_context_data(results=results))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Search"
        context["kg_name"] = kg_name
        context["institute_name"] = institute_name
        if "results" in kwargs:
            context["results"] = kwargs["results"]
        return context
