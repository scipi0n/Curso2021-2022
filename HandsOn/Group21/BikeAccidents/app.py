from flask import Flask, render_template, request, flash
from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"


g = Graph()
g.namespace_manager.bind('owl', Namespace("http://www.w3.org/2002/07/owl#"), override=False)
g.namespace_manager.bind('rdf', Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"), override=False)
g.namespace_manager.bind('rdfs', Namespace("http://www.w3.org/2000/01/rdf-schema#"), override=False)
g.namespace_manager.bind('dbo', Namespace("http://www.traffic-accidents.linkeddata.es/Accidentes#"), override=False)
g.namespace_manager.bind('wdt', Namespace("http://www.wikidata.org/prop/direct/"), override=False)
g.namespace_manager.bind('wd', Namespace("http://www.wikidata.org/entity/"), override=False)

g.parse("BikeAccidents/rdf-with-links.nt", format="ttl")

from rdflib.plugins.sparql import prepareQuery

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dbo = Namespace("http://www.traffic-accidents.linkeddata.es/Accidentes#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
wdt = Namespace("http://www.wikidata.org/prop/direct/")
wd = Namespace("http://www.wikidata.org/entity/")

@app.route("/")
def index():

	q1 = prepareQuery('''
	SELECT Distinct ?distrito 
	WHERE{
    	?accident rdf:type dbo:Accident.
	    ?accident dbo:hasDistrict ?district.
	    ?district rdf:type dbo:District.
	    ?district dbo:hasDistrict ?distrito. 
	}
	'''
	,initNs = {"dbo" : dbo, "rdf" : rdf}
	)

	data = []
	for r in g.query(q1):
		data.append(r.distrito)

	qw = prepareQuery('''
	SELECT Distinct ?weather 
	WHERE{
    	?accident rdf:type dbo:Accident.
	    ?accident dbo:hasWeather ?weather.
	}
	'''
	,initNs = {"dbo" : dbo, "rdf" : rdf}
	)

	weather = []
	for w in g.query(qw):
		weather.append(w.weather)

	qt = prepareQuery('''
	SELECT Distinct ?caida 
	WHERE{
    	?accident rdf:type dbo:Accident.
	    ?accident dbo:hasAccidentType ?caida.
	}
	'''
	,initNs = {"dbo" : dbo, "rdf" : rdf}
	)

	tipoC = []
	for t in g.query(qt):
		tipoC.append(t.caida)

	return render_template('index.html',data=data, weather=weather, tipoC=tipoC)



@app.route("/district", methods=['POST', 'GET'])
def district():
	select_d = request.form.get('district_select')
	select_w = request.form.get('weather_select')
	select_t = request.form.get('tipoC_select')


	#numero accidentes distrito
	q2 = prepareQuery('''
 	SELECT ?accident
	WHERE{
	    ?accident rdf:type dbo:Accident.
	    ?accident dbo:hasDistrict ?district.
	    ?district rdf:type dbo:District.
	    ?district dbo:hasDistrict ?distrito.
	}
  	'''
  	,initNs = {"dbo" : dbo, "rdf" : rdf}
	)

	count = 0;
	for s in g.query(q2, initBindings={'?distrito': Literal(str(select_d), datatype=XSD.string)}):
  		count += 1

  	#numero accidentes distrito
	full_query = prepareQuery('''
 	SELECT  ?lesividad ?fecha ?calle
	WHERE{
    ?accident rdf:type dbo:Accident.

    ?accident dbo:hasWeather ?weather.

    ?accident dbo:hasDistrict ?district.
    ?district rdf:type dbo:District.
    ?district dbo:hasDistrict ?distrito.

    ?accident dbo:hasAccidentType ?tipoC.
     ?accident dbo:hasLesividad ?lesividad.

    ?accident dbo:hasDate ?fecha.

    OPTIONAL{
    ?accident dbo:hasAddress ?address.
    ?address rdf:type dbo:Address.
    ?address dbo:hasAddress ?calle.
    }
}
  	'''
  	,initNs = {"dbo" : dbo, "rdf" : rdf, "owl" : owl}
	)

	ls = []
	fs = []
	calles = []

	for f in g.query(full_query, initBindings={'?distrito': Literal(str(select_d), datatype=XSD.string), 
		'?weather': Literal(str(select_w), datatype=XSD.string), '?tipoC': Literal(str(select_t), datatype=XSD.string)}):
		ls.append(str(f.lesividad))
		fs.append(str(f.fecha))
		calles.append(str(f.calle))





  	#obtener id de distrito wikidata
	q3 = prepareQuery('''
 	SELECT Distinct ?sameDistrict
	WHERE{
	    ?accident rdf:type dbo:Accident.
	    ?accident dbo:hasDistrict ?district.
	    ?district rdf:type dbo:District.
	    ?district dbo:hasDistrict ?distrito.
	    ?district owl:sameAs ?sameDistrict.
    
	}
  	'''
  	,initNs = {"dbo" : dbo, "rdf" : rdf, "owl" : owl}
	)

	for t in g.query(q3, initBindings={'?distrito': Literal(str(select_d), datatype=XSD.string)}):
		link_ent = t.sameDistrict

	#porcentaje
	sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
	query_p1='''
	SELECT ?pop
	WHERE {
	'''
	query_p2="wd:"+link_ent[28:]
	query_p3=''' wdt:P1082 ?pop.
		}'''
	sparql.setQuery(query_p1+query_p2+query_p3)
	sparql.setReturnFormat(JSON)
	res = sparql.query().convert()
	res_frame = pd.io.json.json_normalize(res['results']['bindings'])
	population = res_frame.at[0,'pop.value']

	porcentage = ((count * 1000) / int(population))
	query_p1='''
	SELECT ?img
	WHERE {
	'''
	query_p2="wd:"+link_ent[28:]
	query_p3=''' wdt:P18 ?img.
		}'''
	sparql.setQuery(query_p1+query_p2+query_p3)
	sparql.setReturnFormat(JSON)
	res = sparql.query().convert()
	res_frame = pd.io.json.json_normalize(res['results']['bindings'])
	img = res_frame.at[0,'img.value']

	query_p1='''
	SELECT ?locate
	WHERE {
	'''
	query_p2="wd:"+link_ent[28:]
	query_p3=''' wdt:P242 ?locate.
		}'''
	sparql.setQuery(query_p1+query_p2+query_p3)
	sparql.setReturnFormat(JSON)
	res = sparql.query().convert()
	res_frame = pd.io.json.json_normalize(res['results']['bindings'])
	locate = res_frame.at[0,'locate.value']


	return render_template('district.html',barrio=str(select_d), porcentage=str(porcentage), calles=calles, ls=ls, fs=fs, 
		tiempo = str(select_w), tipoC = str(select_t), count=count, img=img, locate=locate)	

