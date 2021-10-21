# -*- coding: utf-8 -*-

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

salida = "./output.nt"
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://www.calidadAire.com#"), override=False)
g.parse(salida, format="nt")

ns = Namespace("http://www.calidadAire.com#")

from rdflib.plugins.sparql import prepareQuery

# ------------------------------------------

# List all the properties used in our dataset

print("------- Properties 1:")

q = prepareQuery('''
    SELECT DISTINCT ?municipio
    WHERE {
  		 ?provincia ns:tieneMunicipio ?municipio.
    }
    ''',
    initNs = {"ns": ns}
)

for s in g.query(q):
    print(s)
