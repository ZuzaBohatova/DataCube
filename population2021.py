#!/usr/bin/env python3
import csv
from unidecode import unidecode
from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import QB, RDF, XSD, DCTERMS, SKOS

#vytvořím jednotlivé namespaces
NS = Namespace("https://github.com/ZuzaBohatova/DataCube/ontology#")
NSR = Namespace("https://github.com/ZuzaBohatova/DataCube/resources/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SDMXDIMENSION = Namespace("http://purl.org/linked-data/sdmx/2009/dimension#")
SDMXMEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")



def main():
    data_as_csv = load_csv_file_as_object("./data/preparedDataPopulation2021.csv")
    data_cube = as_data_cube(data_as_csv)
    with open("./data/population2021.ttl", "w",encoding="utf-8") as stream:
        stream.write(data_cube.serialize(format="ttl"))


def load_csv_file_as_object(file_path: str):
    result = []
    with open(file_path, "r", encoding="utf-8") as stream:
        reader = csv.reader(stream)
        header = next(reader)  # Skip header
        for line in reader:
            result.append({key: value for key, value in zip(header, line)})
    return result

def as_data_cube(data):
    result = Graph()
    dimensions = create_dimensions(result)
    measures = create_measure(result)
    structure = create_structure(result, dimensions, measures)
    dataset = create_dataset(result, structure)
    create_observations(result, dataset, data)
    return result


def create_dimensions(collector: Graph):

    county = NS.county
    collector.add((county, RDF.type, RDFS.Property))
    collector.add((county, RDF.type, QB.DimensionProperty))
    collector.add((county, SKOS.prefLabel, Literal("Okres", lang="cs")))
    collector.add((county, SKOS.prefLabel, Literal("County", lang="en")))
    collector.add((county, RDFS.subPropertyOf, SDMXDIMENSION.refArea))
    collector.add((county, RDFS.range, XSD.string))

    region = NS.region
    collector.add((region, RDF.type, RDFS.Property))
    collector.add((region, RDF.type, QB.DimensionProperty))
    collector.add((region, SKOS.prefLabel, Literal("Kraj", lang="cs")))
    collector.add((region, SKOS.prefLabel, Literal("Region", lang="en")))
    collector.add((region, RDFS.subPropertyOf, SDMXDIMENSION.refArea))
    collector.add((region, RDFS.range, XSD.string))

    return [county, region]

def create_measure(collector: Graph):

    meanPopulation = NS.meanPopulation
    collector.add(( meanPopulation, RDF.type, RDFS.Property))
    collector.add(( meanPopulation, RDF.type, QB.MeasureProperty))
    collector.add(( meanPopulation, SKOS.prefLabel, Literal("Střední stav obyvatel", lang="cs")))
    collector.add(( meanPopulation, SKOS.prefLabel, Literal("Mean population", lang="en")))
    collector.add(( meanPopulation, RDFS.subPropertyOf, SDMXDIMENSION.obsValue))
    collector.add(( meanPopulation, RDFS.range, XSD.integer))

    return [meanPopulation]

def create_structure(collector: Graph, dimensions, measures):

    structure = NS.structure
    collector.add( ( structure, RDF.type, QB.MeasureProperty ) )

    for dimension in dimensions:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.dimension, dimension))

    for measure in measures:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.measure, measure))

    return structure

def create_dataset(collector: Graph, structure):

    dataset = NSR.dataCubeInstance
    collector.add((dataset, RDF.type, QB.DataSet))
    collector.add((dataset, DCTERMS.publisher, URIRef("https://github.com/ZuzaBohatova/")))
    collector.add((dataset, DCTERMS.available, Literal("2023-03-13", datatype=XSD.date)))
    collector.add((dataset, DCTERMS.language, Literal("cs", datatype=XSD.language)))
    collector.add((dataset, DCTERMS.language, Literal("en", datatype=XSD.language)))
    collector.add((dataset, DCTERMS.license, URIRef("https://https://github.com/ZuzaBohatova/DataCube/blob/main/LICENSE")))
    collector.add((dataset, SKOS.prefLabel, Literal("Střední stav obyvatel", lang="cs")))
    collector.add((dataset, SKOS.prefLabel, Literal("Mean population", lang="en")))
    collector.add((dataset, QB.structure, structure))

    return dataset

def create_observations(collector: Graph, dataset, data):
    for index, row in enumerate(data):
        resource = NSR["observation-" + str(index).zfill(3)]
        create_observation(collector, dataset, resource, row)


def create_observation(collector: Graph, dataset, resource, data):
    collector.add((resource, RDF.type, QB.Observation))
    collector.add((resource, QB.dataSet, dataset))
    county_iri = NS + unidecode(data["okres"].replace(" ", ""))
    region_iri = NS + unidecode(data["kraj"].replace(" ", ""))
    meanPopulation_iri = NS + data["hodnota"].replace(" ","")
    collector.add((resource, NS.county, URIRef(county_iri)))
    collector.add((resource, NS.region, URIRef(region_iri)))
    collector.add((resource, NS.meanPopulation, URIRef(meanPopulation_iri)))
    
    collector.add((URIRef(county_iri), SKOS.prefLabel, Literal(data["okres"], lang="cs")))
    collector.add((URIRef(region_iri), SKOS.prefLabel, Literal(data["kraj"], lang="cs")))

if __name__ == "__main__":
    main()

