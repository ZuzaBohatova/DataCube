#!/usr/bin/env python3

import pandas as pd

#načteme data pro pohyb obyvatel a potřebujeme získat mean population, kde "vuk" == DEM0004
codelist = pd.read_csv("./data/číselník-okresů-vazba-101-nadřízený.csv")
dtPopulation = pd.read_csv("./data/130141-22data2021.csv")

vukDEM0004 = dtPopulation[dtPopulation["vuk"] == "DEM0004"]

#vyberu pouze vuzemi 100 a 101
vuzemi_cis100_101 = vukDEM0004[vukDEM0004.vuzemi_cis.isin([101, 100])]

#convertuju původní kod na nový z codelistu - zmerguju obě dvě datové sady

mergedData = vuzemi_cis100_101.merge(codelist, left_on="vuzemi_kod", right_on="CHODNOTA2")

#chybí mi názvy krajů, tak připojím další soubor 
regions = pd.read_csv("./data/VAZ0108_0109_CS.csv")
preparedData = mergedData.merge(regions, left_on="CHODNOTA1", right_on="chodnota2")

#přejmenuju text1 a text2 na názvy krajů, pro lepší orientaci v datech
preparedData.rename(columns={"text1": "kraj", "text2":"okres"}, inplace=True)
preparedData.to_csv("./data/preparedDataPopulation2021.csv")

