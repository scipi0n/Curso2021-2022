from rdflib import Graph, Namespace, Literal, RDF, RDFS, XSD
from rdflib.plugins.sparql import prepareQuery

file = "https://github.com/MarcoAS99/Curso2021-2022/blob/cdfb4345002cf47e67cd5fcf71487ca4fcfa93f4/HandsOn/Group03/rdf/recycle_triples.nt"
out = []

g = Graph()
g.namespace_manager.bind(
    'rc', Namespace("http://smartcity.smartbins.es/lcc/ontology/recycle#"), override=False)
g.namespace_manager.bind(
    'rdf', Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"), override=False)
g.parse(source=file, format="nt")

rc = Namespace("http://smartcity.smartbins.es/lcc/ontology/recycle#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

q1 = prepareQuery(
    '''
    SELECT DISTINCT ?Bin WHERE{
        ?Bin rdf:type rc:Bin.
    }
    ''',
    initNs={
        "rdf": rdf,
        "rc": rc
    }
)

q2 = prepareQuery(
    '''
    SELECT DISTINCT ?Product WHERE{
        ?Product rdf:type rc:Product.
    } ORDER BY asc(?Product)
    ''',
    initNs={
        "rdf": rdf,
        "rc": rc
    }
)

# for r in g.query(q1):
#     out.append(r.Bin.toPython())

for r in g.query(q2):
    out.append(r.Product.toPython())

print(out[:10])
