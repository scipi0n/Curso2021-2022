# Query 5
from SPARQLWrapper import SPARQLWrapper, XML

sparql = SPARQLWrapper("https://dbpedia.org/sparql")

sparql.setQuery("""
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://dbpedia.org/resource/>
PREFIX dbpedia2: <http://dbpedia.org/property/>
PREFIX dbpedia: <http://dbpedia.org/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dbonto: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?property count(?property) as ?counter 
WHERE {
    ?x a dbonto:Politician .
    ?x ?property ?counter
    MINUS
    {FILTER(?property=rdf:type)}
} LIMIT 20
""")
try:
    sparql.setReturnFormat(XML)
    results = sparql.query().convert()
    print(results.toxml())
except:
    print(Exception)

