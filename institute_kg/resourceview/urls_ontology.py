from django.urls import path

from . import views

urlpatterns = [
    path("<path:resource_name>", views.OntologyView.as_view(), name="ontology"),
]