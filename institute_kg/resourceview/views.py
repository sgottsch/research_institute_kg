from django.http import Http404, HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic import TemplateView, View

from config import kg_name, institute_name
from rdf.rdf_connector import rdf_connector

from model.triple import ValueDatatype


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        target = request.GET.get("href", "")
        target_name = target.split("/")[-1]
        return HttpResponseRedirect(
            reverse("resource", kwargs={"resource_name": target_name})
        )


class ResourceView(TemplateView):

    template_name = "resourceview/resource.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if not self.kwargs.get("resource_name"):
            raise Http404
        resource = rdf_connector.get_resource_by_name(self.kwargs.get("resource_name"))
        if not resource:
            raise Http404
        # set image if exists in triples
        for triple in resource.triples:
            print(triple)
            if triple.value.datatype == ValueDatatype.IMAGE:
                context.update({"image": triple.value.value})
                break
        context.update({"title": resource.pref_label, "resource": resource})
        return context


class OntologyView(TemplateView):
    template_name = "resourceview/resource.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        resource = rdf_connector.get_ontology_resource_by_name(
            self.kwargs.get("resource_name")
        )
        if not resource:
            raise Http404
        context.update(
            {"title": self.kwargs.get("resource_name"), "resource": resource, "kg_name": kg_name, "institute_name": institute_name}
        )
        return context
