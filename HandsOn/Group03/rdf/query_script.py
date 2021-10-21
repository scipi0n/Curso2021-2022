from rdflib import Graph, Namespace, Literal, RDF, RDFS, XSD
from rdflib.plugins.sparql import prepareQuery

github_rep = ""
out = ""

g = Graph()
g.parse(github_rep, format="nt")

rc = Namespace("http://smartcity.smartbins.es/lcc/ontology/recycle#")

q1 = prepareQuery(
    '''
    SELECT DISTINCT ?Bin WHERE{
        ?Bin rdf:Type rc:Bin.
    }
    ''',
    initNs={
        "rdf": RDF,
        "rc": rc
    }
)

for r in g.query(q1):
    out.append(r.Bin)
