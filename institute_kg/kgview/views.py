import json

from django.views.generic import TemplateView

from config import role_types, kg_name, institute_name
from kgcreation.rdf.InstO import InstO
from rdf.graph_converter import convert_to_json
from rdf.rdf_connector import rdf_connector
from rdflib import SDO


class KGView(TemplateView):
    template_name = "kgview/index.html"
    filtered_types = None
    property_filter = "?p"
    title = "Knowledge Graph"
    delete_unconnected_nodes = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        graph = convert_to_json(
            rdf_connector.g,
            type_filter=self.filtered_types,
            property_filter=self.property_filter,
            delete_unconnected_nodes=self.delete_unconnected_nodes,
        )
        context["kg_name"] = kg_name
        context["institute_name"] = institute_name
        context["title"] = self.title
        context["graph"] = json.dumps(graph)
        return context


class KGPeopleView(KGView):
    title = "Co-Author Graph"
    filtered_types = role_types
    delete_unconnected_nodes = True


class KGLocationView(KGView):
    title = "Location Graph"
    filtered_types = role_types | {SDO.City}
    property_filter = SDO.location
    delete_unconnected_nodes = True


class KGLanguageView(KGView):
    title = "Language Graph"
    filtered_types = role_types | {SDO.Language}
    property_filter = SDO.knowsLanguage
    delete_unconnected_nodes = True


class KGWorkplaceView(KGView):
    title = "Workplace Graph"
    filtered_types = role_types | {SDO.House}
    property_filter = SDO.workLocation
    delete_unconnected_nodes = True


class KGResearchFieldView(KGView):
    title = "Research Field Graph"
    filtered_types = role_types | {InstO.ResearchField}
    property_filter = InstO.interest
    delete_unconnected_nodes = True


class KGPaperView(KGView):
    title = "Paper Graph"
    filtered_types = role_types | {SDO.ScholarlyArticle}
    property_filter = SDO.author
    delete_unconnected_nodes = True


class KGConferenceAuthorView(KGView):
    title = "Conference Author Graph"
    filtered_types = role_types | {SDO.Event}
    property_filter = SDO.author
    delete_unconnected_nodes = True


class KGJournalAuthorView(KGView):
    title = "Journal Author Graph"
    filtered_types = role_types | {SDO.Periodical}
    property_filter = SDO.author
    delete_unconnected_nodes = True
