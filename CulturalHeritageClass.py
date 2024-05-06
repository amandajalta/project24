from rdflib import Graph, URIRef, Literal
from pandas import read_csv
from rdflib.namespace import RDF
import pandas as pd

class CulturalHeritageObject:
    def __init__(self, type, title, date, author, owner, place):
        self.type = type
        self.title = title
        self.date = date
        self.author = author
        self.owner = owner
        self.place = place

class Map(CulturalHeritageObject):
    pass

class ManuscriptPlate(CulturalHeritageObject):
    pass

class ManuscriptVolume(CulturalHeritageObject):
    pass

class PrintedVolume(CulturalHeritageObject):
    pass

class PrintedMaterial(CulturalHeritageObject):
    pass

class Herbarium(CulturalHeritageObject):
    pass

class Specimen(CulturalHeritageObject):
    pass

class Painting(CulturalHeritageObject):
    pass

class Model(CulturalHeritageObject):
    pass

class Map(CulturalHeritageObject):
    pass


# Create an empty RDF graph
my_graph = Graph()

# Classes of resources of CulturalHeritageObject
NauticalChart = URIRef("https://schema.org/Map")
ManuscriptPlate = URIRef("https://schema.org/DigitalDocument")
ManuscriptVolume = URIRef("https://schema.org/Book")
PrintedVolume = URIRef("https://schema.org/Book")
PrintedMaterial = URIRef("https://schema.org/CreativeWork")
Herbarium = URIRef("https://schema.org/Herbarium")
Specimen = URIRef("https://schema.org/Specimen")
Painting = URIRef("https://schema.org/Painting")
Model = URIRef("https://schema.org/Model")
Map = URIRef("https://schema.org/Map")

# Attributes related to classes
title = URIRef("https://schema.org/name")
date = URIRef("https://schema.org/dateCreated")
owner = URIRef("https://schema.org/provider")
place = URIRef("https://schema.org/contentLocation")

# Relations among classes
hasAuthor = URIRef("https://schema.org/isPartOf")

# This is the string defining the base URL used to define
# the URLs of all the resources created from the data
base_url = "https://github.com/katyakrsn/ds24project"

# Read CSV file containing this data
file_path_csv = "/Users/amandaaltamirano/Documents/GitHub/2023-2024/docs/Project/data/meta.csv"
heritage = read_csv(
    file_path_csv,
    keep_default_na=False, # Prevent pandas from treating certain values as NaN
    dtype={
        "Id": "string",
        "Type": "string",
        "Title": "string",
        "Date": "string",
        "Author": "string",
        "Owner": "string",
        "Place": "string",
    },
)

# Iterate over each row in the CSV file
for idx, row in heritage.iterrows():
    # Determine the class URI based on the type of CulturalHeritageObject
    class_uri = None
    if row["Type"] == "Nautical chart":
        class_uri = NauticalChart
    elif row["Type"] == "Manuscript plate":
        class_uri = ManuscriptPlate
    elif row["Type"] == "Manuscript volume":
        class_uri = ManuscriptVolume
    elif row["Type"] == "Printed volume":
        class_uri = PrintedVolume
    elif row["Type"] == "Printed material":
        class_uri = PrintedMaterial
    elif row["Type"] == "Herbarium":
        class_uri = Herbarium
    elif row["Type"] == "Specimen":
        class_uri = Specimen
    elif row["Type"] == "Painting":
        class_uri = Painting
    elif row["Type"] == "Model":
        class_uri = Model
    elif row["Type"] == "Map":
        class_uri = Map

    # Create a URI for the resource using the base URL and the row ID
    resource_uri = URIRef(f"{base_url}{row['Id']}")
    
    # Handle missing date values by assigning a default value
    if not row["Date"]:
        row["Date"] = "Unknown"
        print(f"Missing Date at index {idx}")
    
    # Add triples to the graph
    my_graph.add((resource_uri, RDF.type, class_uri))
    my_graph.add((resource_uri, title, Literal(row["Title"])))
    my_graph.add((resource_uri, date, Literal(row["Date"])))
    my_graph.add((resource_uri, owner, Literal(row["Owner"])))
    my_graph.add((resource_uri, place, Literal(row["Place"])))

    # Check for missing author and assign default value if necessary
    if not row["Author"]:
        row["Author"] = "Unknown"
        print(f"Missing Author at index {idx}")
    
    # Add relation among classes if applicable
    if row["Author"]:
        my_graph.add((resource_uri, hasAuthor, Literal(row["Author"])))
    
print("-- Number of triples added to the graph after processing the venues")
print(len(my_graph))


from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
# Initialize SPARQLUpdateStore to interact with Blazegraph
store = SPARQLUpdateStore()
# Define SPARQL endpoint
endpoint = 'http://127.0.0.1:9999/blazegraph/sparql'
# Open connection with SPARQL endpoint
store.open((endpoint, endpoint))
# Upload triples to the Blazegraph database
for triple in my_graph.triples((None, None, None)):
   store.add(triple)
# Close the connection
store.close()

import requests
# Define the SPARQL query
sparql_query = """
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object .
    } 
    ORDER BY ASC(xsd:integer(REPLACE(str(?subject), "https://github.com/katyakrsn/ds24projectdata-", "")))
"""
#REPLACE function to remove the common prefix "https://github.com/katyakrsn/ds24projectdata-" from the subject URIs, leaving only the numerical part.
#xsd:integer(...)  converts the extracted numerical part into an integer datatype.
# ASC keyword specifies that the results should be ordered in ascending order based on the numerical values obtained from the subject URIs.

# Define the Blazegraph SPARQL endpoint URL
sparql_endpoint = 'http://127.0.0.1:9999/blazegraph/sparql'

# Send the SPARQL query to the Blazegraph endpoint
response = requests.post(sparql_endpoint, data={'query': sparql_query})

# Check if the request was successful
if response.status_code == 200:
    # Print the results
    print(response.text)
else:
    print(f"Error: {response.status_code} - {response.reason}")