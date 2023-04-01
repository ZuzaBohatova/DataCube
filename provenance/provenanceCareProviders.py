#!/usr/bin/env python3

from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD, PROV, FOAF, RDFS

#vytvořím jednotlivé namespaces
NS = Namespace("https://github.com/ZuzaBohatova/DataCube/provenance#")
NSR = Namespace("https://github.com/ZuzaBohatova/DataCube/resources/")
mbox = Namespace("mailto:")


def main():
    provenance = create_provenance()
    with open("./provenanceCareProviders.trig", "w",encoding="utf-8") as stream:
        stream.write(provenance.serialize(format="trig"))

def create_provenance():
    result = Graph(bind_namespaces="rdflib")

    create_entities(result)
    create_agents(result)
    create_activities(result)

    return result

def create_entities(collector: Graph):
    dataCube = NSR.CareProvidersDataCube
    datasetPreparedData = NSR.CareProvidersPreparedDataset
    dataset = NSR.CareProvidersDataset

    collector.add((dataCube, RDF.type, PROV.Entity))
    collector.add((dataCube, PROV.wasGeneratedBy, NS.CareProvidersDataCubeCreating))
    collector.add((dataCube, PROV.wasDerivedFrom, datasetPreparedData))
    collector.add((dataCube, PROV.wasAttributedTo, NS.ScriptCareProviders))
    collector.add((dataCube, RDFS.label, Literal("Vygenerovaná data cube Care Providers", lang="cs")))
    collector.add((dataCube, PROV.atLocation, URIRef("file://careProviders.ttl")))
    collector.add((URIRef("file://careProviders.ttl"), RDF.type, PROV.Location))
    
    collector.add((datasetPreparedData, RDF.type, PROV.Entity))
    collector.add((datasetPreparedData, PROV.wasAttributedTo, NS.ScriptPrepareDataCareProviders))
    collector.add((datasetPreparedData, PROV.wasGeneratedBy, NS.CareProvidersPreparingData))
    collector.add((datasetPreparedData, PROV.wasDerivedFrom, dataset))
    collector.add((datasetPreparedData, RDFS.label, Literal("Připravená data pro zpracování", lang="cs")))
    collector.add((datasetPreparedData, PROV.atLocation, URIRef("file://preparedDataCareProviders.py")))
    collector.add((URIRef("file://preparedDataCareProviders.py"), RDF.type, PROV.Location))

    collector.add((dataset, RDF.type, PROV.Entity))
    collector.add((dataset, RDFS.label, Literal("Původní data od Ministerstva Zdravotnictví", lang="cs")))
    collector.add((dataset, PROV.atLocation, URIRef("file://narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv")))
    collector.add((URIRef("file://narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv"), RDF.type, PROV.Location))


def create_agents(collector: Graph):
    creator = NS.ZuzanaBohatova
    supervisor = NS.PetrSkoda
    university = NS.MffUK
    script = NS.ScriptCareProviders
    scriptPrepareData = NS.ScriptPrepareDataCareProviders

    collector.add((scriptPrepareData, RDF.type, PROV.SoftwareAgent))
    collector.add((scriptPrepareData, RDFS.label, Literal("Script prepareDataCareProviders.py připravující data ke zpracování", lang="cs")))
    collector.add((scriptPrepareData, PROV.actedOnBehalfOf, creator))
    collector.add((scriptPrepareData, PROV.atLocation, URIRef("file://prepareDataCareProviders.py")))
    collector.add((URIRef("file://prepareDataCareProviders.py"), RDF.type, PROV.Location))

    collector.add((script, RDF.type, PROV.SoftwareAgent))
    collector.add((script, RDFS.label, Literal("Script careProviders.py generující data cube", lang="cs")))
    collector.add((script, PROV.actedOnBehalfOf, creator))
    collector.add((script, PROV.atLocation, URIRef("file://careProviders.py")))
    collector.add((URIRef("file://careProviders.py"), RDF.type, PROV.Location))


    collector.add((creator, RDF.type, PROV.Agent))
    collector.add((creator, RDF.type, PROV.Person))
    collector.add((creator, FOAF.name, Literal("Zuzana Bohatová", lang="cs")))
    collector.add((creator, FOAF.mbox, mbox["zuzana.bohatova@email.cz"]))
    collector.add((creator, PROV.actedOnBehalfOf, supervisor))
    collector.add((creator, FOAF.homepage, Literal("https://github.com/ZuzaBohatova/", datatype=XSD.anyURI)))

    collector.add((supervisor, RDF.type, PROV.Agent))
    collector.add((supervisor, RDF.type, PROV.Person))
    collector.add((supervisor, FOAF.name, Literal("Petr Škoda", lang="cs")))
    collector.add((supervisor, FOAF.mbox, mbox["petr.skoda@matfyz.cuni.cz"]))
    collector.add((supervisor, PROV.actedOnBehalfOf, university))
    collector.add((supervisor, FOAF.homepage, Literal("https://skodapetr.github.io/", datatype=XSD.anyURI)))

    collector.add((university, RDF.type, FOAF.Organization))
    collector.add((university, RDF.type, PROV.Agent))
    collector.add((university, FOAF.name, Literal("Matematicko-fyzikální fakulta, Univerzita Karlova", lang="cs")))
    collector.add((university, FOAF.schoolHomepage, Literal("https://www.mff.cuni.cz/", datatype=XSD.anyURI)))

def create_activities(collector: Graph):

    preparingData = NS.CareProvidersPreparingData
    usagePreparingData = BNode()
    collector.add((usagePreparingData, RDF.type, PROV.Usage))
    collector.add((usagePreparingData, PROV.entity, NSR.CareProvidersDataset))
    collector.add((usagePreparingData, PROV.hadRole, NS.PythonScript))

    collector.add((preparingData, RDF.type, PROV.Activity)) 
    collector.add((preparingData, PROV.qualifiedUsage, usagePreparingData))
    collector.add((preparingData, PROV.generated, NSR.CareProvidersPreparedDataset))
    collector.add((preparingData, PROV.used, NSR.CareProvidersDataset))
    collector.add((preparingData, PROV.wasAssociatedWith, NS.ZuzanaBohatova))

    dataCubeCreating = NS.CareProvidersDataCubeCreating
    usageCreatingDataCube = BNode()

    collector.add((usageCreatingDataCube, RDF.type, PROV.Usage))
    collector.add((usageCreatingDataCube, PROV.entity, NSR.CareProvidersPreparedDataset))
    collector.add((usageCreatingDataCube, PROV.hadRole, NS.PythonScript))

    collector.add((dataCubeCreating, RDF.type, PROV.Activity)) 
    collector.add((dataCubeCreating, PROV.qualifiedUsage, usageCreatingDataCube))
    collector.add((dataCubeCreating, PROV.generated, NSR.CareProvidersDataCube))
    collector.add((dataCubeCreating, PROV.used, NSR.CareProvidersPreparedDataset))
    collector.add((dataCubeCreating, PROV.wasAssociatedWith, NS.ZuzanaBohatova))

    collector.add((NS.PythonScript, RDF.type, PROV.Role))


if __name__ == "__main__":
    main()