# DataCube
Zde najdete zadaní úkolu. 
https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02-data-cube.html
Cílem je vytvořit dvě data cubes a poté otestovat jejich integritní omezení.

## System requirements
Nutné mít nainstalovaný Python >= 3.8 a knihovny, které jsou uloženy v souboru requirements.txt 

## Instalace
1. nejprve si naklonujte nebo stáhněte tento repozotář
2. poté nainstalujte requirements příkazem: pip instal -r requirements.txt 
3. spusťte dané soubory: python careProviders.py a python population2021.py
4. až po provedení bodu 3. můžete spustit python integrityConstraints.py

## Příprava dat
V adresáři data/ jsou uložena všechna zdrojová data pro python scripty. Všechna data jsem získávala z portálu data.gov.cz
### Care Providers
Vytvořila jsem si python script prepareDataCareProciders.py, kde jsem upravila data do potřebné podoby. Výsledná data jsou uložena v adresáři data/ jako preparedDataCR.csv

### Population 2021
Opět jsem si připravila data pomocí python scriptu prepareDataPopulation2021.py. Zde jsme museli mergovat několi csv souborů, abychom získali všechny potřebné informace. Připravená data uložena jako data/preparedDataPopulation.csv

## Scripty
### careProviders.py
Po spuštění vygeneruje data cube do souboru careProviders.ttl. 

### population2021.py
Po spuštění vygeneruje data cube do souboru population2021.ttl.

### integrityConstraints.py
Po stpuštění vezme výsledná data z dvou předchozích scriptů a otestuje všechna integrity constraints, viz zde: https://www.w3.org/TR/vocab-data-cube/#h3_wf-rules . Výsledek vypíše na standartní výstup. V případě, že je výsledek pro dané omezení False, tak je vše v pořádku. Pokud dotaz vrátí true, tak daná data cube porušuje toto integritní omezení.
(Bohužel se mi nepodařilo správně přidat declaraci slice, tak pro tento případ odchytávám chybu, aby celý proces nespadl.) 
