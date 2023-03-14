import pandas as pd

#v původním csv souboru nemám určený data type pro sloupce 14 a 15, tak specifikuji jako string
dtype = {"PoskytovatelTelefon":str, "PoskytovatelFax":str}

#načtení původního csv souboru se specifikovaným dtype
df = pd.read_csv("./data/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv", dtype=dtype)

#provedu groupBy přes všechny tři dimenze ze zadání a potřebuju konkrétní číslo počtu poskytovatelů
newFile = df.groupby(["Okres", "Kraj", "OborPece"]).size().reset_index(name="PocetPoskytovatelu")

#připravená data vložím do souboru preparedDataCR  
newFile.to_csv("./data/preparedDataCR.csv")
