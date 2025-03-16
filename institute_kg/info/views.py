from django.shortcuts import render

from config import institute_name, website_contacts, kg_name, example_resource_id

SITE_ABOUT = "about"

def index(request):
    context = {"kg_name": kg_name, "example_resource_id": example_resource_id}
    return render(request, "info/index.html", context)

def about(request):
    context = {"title": "About", "site": SITE_ABOUT, "contacts": website_contacts, "kg_name": kg_name, "institute_name": institute_name}

    return render(request, "info/about.html", context)