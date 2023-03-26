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



def main(outputfile):
    data_as_csv = load_csv_file_as_object("./preparedDataCR.csv")
    data_cube = as_data_cube(data_as_csv)
    with open(outputfile, "w",encoding="utf-8") as stream:
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
    slices = create_slices(result)
    structure = create_structure(result, dimensions, measures, slices)
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

    fieldOfCare = NS.fieldOfCare
    collector.add((fieldOfCare, RDF.type, RDFS.Property))
    collector.add((fieldOfCare, RDF.type, QB.DimensionProperty))
    collector.add((fieldOfCare, SKOS.prefLabel, Literal("Obor Péče", lang="cs")))
    collector.add((fieldOfCare, SKOS.prefLabel, Literal("Field of care", lang="en")))
    collector.add((fieldOfCare, RDFS.subPropertyOf, SDMXDIMENSION.occupation))
    collector.add((fieldOfCare, RDFS.range, XSD.string))

    return [county, region, fieldOfCare]

def create_measure(collector: Graph):

    numberOfCareProviders = NS.numberOfCareProviders
    collector.add(( numberOfCareProviders, RDF.type, RDFS.Property))
    collector.add(( numberOfCareProviders, RDF.type, QB.MeasureProperty))
    collector.add(( numberOfCareProviders, SKOS.prefLabel, Literal("Počet poskytovatelů péče", lang="cs")))
    collector.add(( numberOfCareProviders, SKOS.prefLabel, Literal("Number of care providers", lang="en")))
    collector.add(( numberOfCareProviders, RDFS.subPropertyOf, SDMXDIMENSION.obsValue))
    collector.add(( numberOfCareProviders, RDFS.range, XSD.integer))

    return [numberOfCareProviders]

def create_slices(collector: Graph):
    slicePsychiatrie = NS.slicePsychiatrie
    collector.add((slicePsychiatrie, RDF.type, QB.sliceKey))
    collector.add((slicePsychiatrie, NS.fieldOfCare, Literal("psychiatrie", datatype=XSD.string)))
    collector.add((slicePsychiatrie, SKOS.prefLabel, Literal("Řez přes počet poskytovatelů péče", lang="cs")))
    collector.add((slicePsychiatrie, SKOS.prefLabel, Literal("Slice by field of care", lang="en")))
    collector.add(( slicePsychiatrie, RDFS.subPropertyOf, SDMXDIMENSION.occupation))
    collector.add(( slicePsychiatrie, RDFS.range, XSD.string))
    return [slicePsychiatrie]


def create_structure(collector: Graph, dimensions, measures, slices):

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

    for sl in slices:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.dimension, sl))

    return structure

def create_dataset(collector: Graph, structure):

    dataset = NSR.dataCubeInstance
    collector.add((dataset, RDF.type, QB.DataSet))
    collector.add((dataset, DCTERMS.publisher, URIRef("https://github.com/ZuzaBohatova/")))
    collector.add((dataset, DCTERMS.available, Literal("2023-03-13", datatype=XSD.date)))
    collector.add((dataset, DCTERMS.language, Literal("cs", datatype=XSD.language)))
    collector.add((dataset, DCTERMS.language, Literal("en", datatype=XSD.language)))
    collector.add((dataset, DCTERMS.license, URIRef("https://https://github.com/ZuzaBohatova/DataCube/blob/main/LICENSE")))
    collector.add((dataset, SKOS.prefLabel, Literal("Počet poskytovatelů péče", lang="cs")))
    collector.add((dataset, SKOS.prefLabel, Literal("Number of care provider", lang="en")))
    collector.add((dataset, QB.structure, structure))

    return dataset

def create_observations(collector: Graph, dataset, data):
    for index, row in enumerate(data):
        resource = NSR["observation-" + str(index).zfill(3)]
        create_observation(collector, dataset, resource, row)


def create_observation(collector: Graph, dataset, resource, data):
    collector.add((resource, RDF.type, QB.Observation))
    collector.add((resource, QB.dataSet, dataset))
    county_iri = NS + unidecode(data["Okres"].replace(" ", ""))
    region_iri = NS + unidecode(data["Kraj"].replace(" ", ""))
    fieldOfCare_iri = NS + unidecode(data["OborPece"].replace(" ","").replace(",","-"))
    numberOfCareProviders_iri = NS + data["PocetPoskytovatelu"]
    collector.add((resource, NS.county, URIRef(county_iri)))
    collector.add((resource, NS.region, URIRef(region_iri)))
    collector.add((resource, NS.fieldOfCare, URIRef(fieldOfCare_iri)))
    collector.add((resource, NS.numberOfCareProviders, URIRef(numberOfCareProviders_iri)))
    if data['OborPece'] == "psychiatrie":
        collector.add((resource, QB.sliceKey, NS.slicePsychiatrie))

if __name__ == "__main__":
    main()

