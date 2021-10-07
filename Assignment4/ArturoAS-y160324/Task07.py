#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib ')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# In[3]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

# In[5]:


from rdflib.plugins.sparql import prepareQuery


print("Parte de RDFLib:")
ns = Namespace("http://somewhere#")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s,p,o)
print() #space
print("SPARQL:")
query = prepareQuery('''
  SELECT DISTINCT ?x
  WHERE{
          ?x (rdfs:subClassOf/rdfs:subClassOf*) ns:Person
          }
          ''',
  initNs = {"rdfs": RDFS, "ns": ns}
)
for i in g.query(query):
  print(i)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[9]:


print("RDFLib:")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2, p2, o2 in g.triples((None, RDF.type, s)):
    print(s2)
print()

print("SPARQL:")
query = prepareQuery('''
  SELECT ?s
  WHERE { 
    { 
      ?s rdf:type ns:Person. 
    } UNION {
      ?subclass rdfs:subClassOf ns:Person.
      ?s rdf:type ?subclass
    }
  }
  ''',
  initNs = { "rdfs": RDFS,"rdf": RDF, "ns": ns}
)
for i in g.query(query):
  print(i)


# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# 

# In[11]:


print("RDFLib:")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for s2, p2, o2 in g.triples((s, None, None)):
    print(s2, p2, o2)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2, p2, o2 in g.triples((None, RDF.type, s)):
    for s3, p3, o3 in g.triples((s2, None, None)):
      print(s3, p3, o3)
    
print()

print("SPARQL:")
query = prepareQuery('''
  SELECT ?s ?o ?p
  WHERE { 
    { 
      ?s rdf:type ns:Person.
      ?s ?o ?p
    } UNION {
      ?s rdf:type ?s1.
      ?s ?o ?p.
      ?s1 rdfs:subClassOf ns:Person
    }
  }
  ''',
  initNs = { "rdfs": RDFS,"rdf": RDF, "ns": ns}
)

for i in g.query(query):
  print(i)
    


# In[ ]:




