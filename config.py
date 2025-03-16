from rdflib import SDO

from kgcreation.rdf.InstO import InstO

# ~~~ DBLP Extractor ~~~

### Cache folder

# A folder where cached dblp results are stored.
# Example: "kgcreation/data/dblp_cache/"
dblp_cache_directory = "kgcreation/data/dblp_cache/"

# ~~~ Wikidata Extractor ~~~

# ID of the Wikidata institute
# Example: "Q1797810"
institute_wikidata_id = "Q1797810"

# ~~~ RDF ~~~

# Prefix of resources in the institute KG.
# Example: "https://l3skg.l3s.uni-hannover.de/resource/"
institute_resource_prefix = "https://l3skg.l3s.uni-hannover.de/resource/"

# Prefix of properties and classes in the institute KG.
# Example: "https://l3skg.l3s.uni-hannover.de/ontology/"
institute_ontology_prefix = "https://l3skg.l3s.uni-hannover.de/ontology/"

# Namespace of resources in the institute KG.
# Example: "l3skg"
institute_resource_namespace = "l3skg"

# Namespace of properties and classes in the institute KG.
# Example: "l3skgo"
institute_ontology_namespace = "l3skgo"

# Label of the property that denotes the start date of the person working at the institute
institute_starting_date_property_label = "L3S start date"

# !IMPORTANT! Add more positions to InstO if needed.

# ~~~ Google Forms Extractor ~~~

# The location of the XLSX file with survey replies as exported from Google Forms.
# Example: "kgcreation/data/input/responses.xlsx"
google_forms_answers_file_name = "kgcreation/data/input/responses.xlsx"

# ~~~ Google Scholar Extractor ~~~

# ID of the institute at Google Scholar
# Example:  "3922818465484085317" (L3S)
google_scholar_institute_id = "3922818465484085317"

# A set of additional Google Scholar IDs of researchers to be added (e.g., from the Google Form).
google_scholar_additional_person_ids = {
        "8f3WFJAAAAAJ",
    }

# A set of Google Scholar IDs of researchers that need to be ignored.
# This set is required in cases where a researchers in Google Scholar has no citations because otherwise there will be an error.
google_scholar_person_ids_to_be_removed = {
        "TXFBhPMAAAAJ"
}

# ~~~ Indexes ~~~

###  City Matching

# A dictionary of city names and how they should be replaced for uniformity.
# Example: "https://de.wikipedia.org/wiki/Hannover": "https://en.wikipedia.org/wiki/Hanover"
# -> If a city is named https://de.wikipedia.org/wiki/Hannover, name it https://en.wikipedia.org/wiki/Hanover instead.
city_matches = {"https://de.wikipedia.org/wiki/Hannover": "https://en.wikipedia.org/wiki/Hanover",
                "https://de.wikipedia.org/wiki/Thessaloniki": "https://en.wikipedia.org/wiki/Thessaloniki",
                "Q3766": "https://en.wikipedia.org/wiki/Damascus", "Q1731": "https://en.wikipedia.org/wiki/Dresden"}

### Buildings

# A dictionary of building names with
# Example: "LL6": "Lange Laube 6"
# -> If a building is named "LL6", name it "Lange Laube 6" instead.
building_matches = { "LL6": "Lange Laube 6"}

### Person names

# A list of name parts which are removed when creating names.
# Example: "Dr." -> The Dr. prefix is removed from a person's name.
person_name_parts_to_remove = {"Dr.", "rer.", "nat.", "ing.", "Jun.-Prof.", "Prof.", "M.", "B.", "Sc.", "Dipl.",
             "-Geogr.", "-Ing.", "Eng.", "Tech.", ","}

### Research Interests
# A dictionary of research interests and how they should be replaced for uniformity.
# Example: "NLP": "Natural Language Processing"
# -> If a research interest is named "NLP", name it "Natural Language Processing" instead.
research_interest_matches = { "NLP": "Natural Language Processing"}

# ~~~ Others ~~~

# File name of the KG to be created.
# Example: "institute_kg.ttl"
institute_kg_file_name = "institute_kg.ttl"

# Name of the default/super class of all person's of the institute in the KG
# Example: "L3S Associate"
institute_super_position = "L3S Associate"

# ~~~ Website ~~~

# Institute name
institute_name = "L3S"

# Name of the KG
kg_name = "L3SKG"

# Contacts: A list of contacts shown oin the websute
# Example: { {"name": "Simon Gottschalk", "email": "gottschalk@L3S.de"}}
website_contacts = [{"name": "FirstName LastName", "email": "first.last@example.org"}]

# URL of the website (used in website settings)
website_url = "https://127.0.0.1:8000"

# End of the URL identifying an example resource
# Example: "SimonGottschalk" -> links to InstR["SimonGottschalk"]
example_resource_id = "SimonGottschalk"

# Allowed hosts (used in website settings)
website_allowed_hosts = [
    'l3skg.l3s.uni-hannover.de',
    '127.0.0.1',
    'localhost'
]

# Website secret key (used in website settings)
website_secret_key = "<KEY>"

# A set of person classes shown in the KG visualisation
role_types = {
    SDO.Person,
    InstO.ResearchGroupLeader,
    InstO.PhDStudent
}

# An Example query
example_query = """# Select all L3S group leaders 

SELECT ?label WHERE {
    ?person rdf:type l3skgo:ResearchGroupLeader .
    ?person rdfs:label ?label .
}"""

# A list of example queries, with a description
example_queries = [
{"query_str":
"""# Select all L3S research group leaders 
 
 SELECT ?label WHERE {
     ?person rdf:type l3skgo:ResearchGroupLeader .
     ?person rdfs:label ?label .
 }""".replace("\n", "@NL@"), "description": "Select all L3S research group leaders."},

{"query_str":
"""# Who hast most co-authors within L3S? 
 
 SELECT ?label ?person  (COUNT(DISTINCT ?coAuthor) AS ?count) WHERE {
     ?person l3skgo:coAuthor ?coAuthor ;
         rdfs:label ?label .
 } 
 GROUP BY ?person
 ORDER BY DESC(COUNT(DISTINCT ?coAuthor))
 LIMIT 1""".replace("\n", "@NL@"), "description": "Who hast most co-authors within L3S?"},

{"query_str":
"""# Statistics of person types 
 
 SELECT ?type  (COUNT(DISTINCT ?person) AS ?count) WHERE {
     ?person rdf:type ?type .
     ?type rdfs:subClassOf l3skgo:L3SAssociate .
 }
 GROUP BY ?type
 ORDER BY DESC(COUNT(DISTINCT ?person))""".replace("\n", "@NL@"),
"description": "Statistics of person types."},
]

# A map from each position to a CSS class
positions_map = {
    InstO.ResearchGroupLeader: "ResearchGroupLeader",
    InstO.PhDStudent: "PhDStudent"
}