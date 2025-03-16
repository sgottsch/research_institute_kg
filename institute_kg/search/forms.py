from django import forms
from rdf.rdf_connector import rdf_connector


def get_types():
    q = """
    SELECT DISTINCT ?type WHERE {
        ?x rdf:type ?type .
    }
    """
    q2 = """
    SELECT DISTINCT ?child ?parent WHERE {
        ?child rdfs:subClassOf ?parent.
    }
    """
    types = []
    for i in rdf_connector.run_query(q):
        types.append(i[0])
    return [(str(i), str(i)) for i in types]


class SearchForm(forms.Form):
    query = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Search…"}),
    )
    # type_filter = forms.ChoiceField(choices=get_types())
