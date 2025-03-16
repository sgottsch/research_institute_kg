from django.urls import path

from . import views

urlpatterns = [
    path("", views.RedirectView.as_view(), name="resource_redirect"),
    path("<path:resource_name>", views.ResourceView.as_view(), name="resource"),
]