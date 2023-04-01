#!/usr/bin/env python3

from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD, PROV, FOAF, RDFS

#vytvořím jednotlivé namespaces
NS = Namespace("https://github.com/ZuzaBohatova/DataCube/provenance#")
NSR = Namespace("https://github.com/ZuzaBohatova/DataCube/resources/")
mbox = Namespace("mailto:")


def main():
    provenance = create_provenance()
    with open("./provenancePopulation2021.trig", "w",encoding="utf-8") as stream:
        stream.write(provenance.serialize(format="trig"))

def create_provenance():
    result = Graph(bind_namespaces="rdflib")

    create_entities(result)
    create_agents(result)
    create_activities(result)

    return result

def create_entities(collector: Graph):
    dataCube = NSR.PopulationDataCube
    datasetPreparedData = NSR.PopulationPreparedDataset
    dataset1 = NSR.PopulationDataset
    dataset2 = NSR.PopulationCodeListDataset
    dataset3 = NSR.PopulationCodeListNameDataset

    collector.add((dataCube, RDF.type, PROV.Entity))
    collector.add((dataCube, PROV.wasGeneratedBy, NS.PopulationDataCubeCreating))
    collector.add((dataCube, PROV.wasDerivedFrom, datasetPreparedData))
    collector.add((dataCube, PROV.wasAttributedTo, NS.ScriptPopulation))
    collector.add((dataCube, RDFS.label, Literal("Vygenerovaná data cube Population 2021", lang="cs")))
    collector.add((dataCube, PROV.atLocation, URIRef("file://population2021.ttl")))
    collector.add((URIRef("file://population2021.ttl"), RDF.type, PROV.Location))
    
    collector.add((datasetPreparedData, RDF.type, PROV.Entity))
    collector.add((datasetPreparedData, PROV.wasAttributedTo, NS.ScriptPreparePopulation))
    collector.add((datasetPreparedData, PROV.wasGeneratedBy, NS.Population2021DataPreparing))
    collector.add((datasetPreparedData, PROV.wasDerivedFrom, dataset1))
    collector.add((datasetPreparedData, PROV.wasDerivedFrom, dataset2))
    collector.add((datasetPreparedData, PROV.wasDerivedFrom, dataset3))
    collector.add((datasetPreparedData, RDFS.label, Literal("Připravená data pro zpracování", lang="cs")))
    collector.add((datasetPreparedData, PROV.atLocation, URIRef("file://preparedDataPopulation2021.py")))
    collector.add((URIRef("file://preparedDataPopulation2021.py"), RDF.type, PROV.Location))

    collector.add((dataset1, RDF.type, PROV.Entity))
    collector.add((dataset1, RDFS.label, Literal("Pohyb obyvatel za ČR, kraje, okresy, SO ORP a obce - rok 2021", lang="cs")))
    collector.add((dataset1, PROV.atLocation, URIRef("file://číselník-okresů-vazba-101-nadřízený.csv")))
    collector.add((URIRef("file://číselník-okresů-vazba-101-nadřízený.csv"), RDF.type, PROV.Location))

    collector.add((dataset2, RDF.type, PROV.Entity))
    collector.add((dataset2, RDFS.label, Literal("Číselník okresů", lang="cs")))
    collector.add((dataset2, PROV.atLocation, URIRef("file://130141-22data2021.csv")))
    collector.add((URIRef("file://130141-22data2021.csv"), RDF.type, PROV.Location))

    collector.add((dataset3, RDF.type, PROV.Entity))
    collector.add((dataset3, RDFS.label, Literal("Číselník okresů s názvy krajů a okresů", lang="cs")))
    collector.add((dataset3, PROV.atLocation, URIRef("file://VAZ0108_0109_CS.csv")))
    collector.add((URIRef("file://VAZ0108_0109_CS.csv"), RDF.type, PROV.Location))


def create_agents(collector: Graph):
    creator = NS.ZuzanaBohatova
    supervisor = NS.PetrSkoda
    university = NS.MffUK
    script = NS.ScriptPopulation
    scriptPrepareData = NS.ScriptPreparePopulation

    collector.add((scriptPrepareData, RDF.type, PROV.SoftwareAgent))
    collector.add((scriptPrepareData, RDFS.label, Literal("Script prepareDataPopulation2021.py připravující data ke zpracování", lang="cs")))
    collector.add((scriptPrepareData, PROV.actedOnBehalfOf, creator))
    collector.add((scriptPrepareData, PROV.atLocation, URIRef("file://prepareDataPopulation2021.py")))
    collector.add((URIRef("file://prepareDataPopulation2021.py"), RDF.type, PROV.Location))

    collector.add((script, RDF.type, PROV.SoftwareAgent))
    collector.add((script, RDFS.label, Literal("Script population2021.py generující data cube", lang="cs")))
    collector.add((script, PROV.actedOnBehalfOf, creator))
    collector.add((script, PROV.atLocation, URIRef("file://population2021.py")))
    collector.add((URIRef("file://population2021.py"), RDF.type, PROV.Location))


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
    preparingData = NS.Population2021DataPreparing
    usagePreparingData3 = BNode()
    usagePreparingData2 = BNode()
    usagePreparingData1 = BNode()

    collector.add((usagePreparingData1, RDF.type, PROV.Usage))
    collector.add((usagePreparingData1, PROV.entity, NSR.PopulationDataset))
    collector.add((usagePreparingData1, PROV.hadRole, NS.PythonScript))

    collector.add((usagePreparingData2, RDF.type, PROV.Usage))
    collector.add((usagePreparingData2, PROV.entity, NSR.PopulationCodeListDataset))
    collector.add((usagePreparingData2, PROV.hadRole, NS.PythonScript))

    collector.add((usagePreparingData3, RDF.type, PROV.Usage))
    collector.add((usagePreparingData3, PROV.entity, NSR.PopulationCodeListNameDataset))
    collector.add((usagePreparingData3, PROV.hadRole, NS.PythonScript))

    collector.add((preparingData, RDF.type, PROV.Activity)) 
    collector.add((preparingData, PROV.qualifiedUsage, usagePreparingData1))
    collector.add((preparingData, PROV.qualifiedUsage, usagePreparingData2))
    collector.add((preparingData, PROV.qualifiedUsage, usagePreparingData3))
    collector.add((preparingData, PROV.generated, NSR.PopulationPreparedDataset))
    collector.add((preparingData, PROV.used, NSR.PopulationDataset))
    collector.add((preparingData, PROV.used, NSR.PopulationCodeListDataset))
    collector.add((preparingData, PROV.used, NSR.PopulationCodeListNameDataset))
    collector.add((preparingData, PROV.wasAssociatedWith, NS.ZuzanaBohatova))

    dataCubeCreating = NS.PopulationDataCubeCreating
    usageCreatingDataCube = BNode() 
    
    collector.add((usageCreatingDataCube, RDF.type, PROV.Usage))
    collector.add((usageCreatingDataCube, PROV.entity, NSR.PopulationPreparedDataset))
    collector.add((usageCreatingDataCube, PROV.hadRole, NS.PythonScript))
    
    collector.add((dataCubeCreating, RDF.type, PROV.Activity)) 
    collector.add((dataCubeCreating, PROV.qualifiedUsage, usageCreatingDataCube))
    collector.add((dataCubeCreating, PROV.generated, NSR.PopulationDataCube))
    collector.add((preparingData, PROV.used, NSR.PopulationPreparedDataset))
    collector.add((preparingData, PROV.wasAssociatedWith, NS.ZuzanaBohatova))


    collector.add((NS.PythonScript, RDF.type, PROV.Role))


if __name__ == "__main__":
    main()