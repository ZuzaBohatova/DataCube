from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.careProviders import produce_data_cube_CareProviders
from scripts.population2021 import produce_data_cube_Population

import pandas as pd
import os

def set_outputPath(fce, **param):
    output_path = param['dag_run'].conf.get("output_path", None)
    if output_path:
        fce(output_path)
    else:
        fce()


default_args = {
    "owner": "Zuzana Bohatova",
    "depends_on_past": False,
    "start_date": datetime(2023, 3, 27),
    "email": ["airflowadmin@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with  DAG(
    dag_id="data-cubes",
    default_args=default_args,
    description="A DAG to produce a data cube",
    schedule=None,
) as dag:

    #Care Providers

    def prepare_data_CareProviders():
        dtype = {"PoskytovatelTelefon":str, "PoskytovatelFax":str}
        df = pd.read_csv("https://data.mzcr.cz/distribuce/63/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv", dtype=dtype)
        newFile = df.groupby(["Okres", "Kraj", "OborPece"]).size().reset_index(name="PocetPoskytovatelu")
        newFile.to_csv("./preparedDataCR.csv")

    prepare_data_CareProviders_task = PythonOperator(
		task_id = "prepare_data_CareProviders_task",
		python_callable = prepare_data_CareProviders,
	)
    produce_data_cube_CareProviders_task = PythonOperator(
		task_id = "produce_data_cube_CareProviders_task",
		python_callable = set_outputPath,
        op_args=[produce_data_cube_CareProviders],
	)

    #Population2021

    def prepare_data_Population():
        import ssl
        import urllib.request

        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/%C4%8D%C3%ADseln%C3%ADk-okres%C5%AF-vazba-101-nad%C5%99%C3%ADzen%C3%BD.csv"
        with urllib.request.urlopen(url) as response:
            codelist = pd.read_csv(response)
        dtPopulation = pd.read_csv("https://www.czso.cz/documents/10180/184344914/130141-22data2021.csv")

        vukDEM0004 = dtPopulation[dtPopulation["vuk"] == "DEM0004"]
        vuzemi_cis100_101 = vukDEM0004[vukDEM0004.vuzemi_cis.isin([101, 100])]

        mergedData = vuzemi_cis100_101.merge(codelist, left_on="vuzemi_kod", right_on="CHODNOTA2")
        regions = pd.read_csv("https://apl.czso.cz/iSMS/do_cis_export?kodcis=108&typdat=1&cisvaz=109_210&cisjaz=203&format=2&separator=%2C")
        preparedData = mergedData.merge(regions, left_on="CHODNOTA1", right_on="chodnota2")

        preparedData.rename(columns={"text1": "kraj", "text2":"okres"}, inplace=True)
        preparedData.to_csv("./preparedDataPopulation2021.csv")

    

    prepare_data_Population_task = PythonOperator(
		task_id = "prepare_data_Population_task",
		python_callable = prepare_data_Population,
	)

    produce_data_cube_Population_task = PythonOperator(
		task_id = "produce_data_cube_Population_task",
		python_callable = set_outputPath,
        op_args=[produce_data_cube_Population],
	)

    prepare_data_CareProviders_task >> produce_data_cube_CareProviders_task
    prepare_data_Population_task >> produce_data_cube_Population_task


