from django.shortcuts import render
from rdflib import RDF

from config import example_query, example_queries, kg_name, institute_name
from rdf.rdf_connector import rdf_connector

SITE_SPARQL = "sparql"


def show_query_result(request):
    query = request.GET.get('query', '')
    html_query = query.replace("\n", "<br>").replace(" ", "&nbsp;")
    context = {"title": "SPARQL Endpoint", "site": SITE_SPARQL, "query": html_query}

    res = rdf_connector.run_query(query)
    print(res.vars)

    context["vars"] = [str(var) for var in res.vars]

    context["results"] = []
    for row in res:
        row_context = []
        for var in res.vars:
            row_context.append(str(row[var]))
        context["results"].append(row_context)
        context["kg_name"] = kg_name
        context["institute_name"] = institute_name


    for a in res:
        print(a)

    return render(request, "sparqlendpoint/result.html", context)


def index(request):

    if request.GET.get('query', ''):
        return show_query_result(request)

    g = rdf_connector.g
    prefixes = []
    for ns_prefix, namespace in g.namespaces():
        prefixes.append({"ns": ns_prefix, "prefix": namespace})

    context = {"title": "SPARQL Endpoint", "site": SITE_SPARQL, "example_query": example_query, "example_queries": example_queries, "prefixes": prefixes}
    return render(request, "sparqlendpoint/index.html", context)
