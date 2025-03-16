from django import template
from django.shortcuts import reverse
from rdf.rdf_connector import PREFIX, PREFIX_ONTOLOGY
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def uri_reverse(value):
    """Redirect URLs of local KG entities"""
    if PREFIX in value:
        return reverse("resource", kwargs={"resource_name": value[len(PREFIX):]})
    if PREFIX_ONTOLOGY in value:
        return reverse("ontology",  kwargs={"resource_name": value[len(PREFIX):]})
    return value
