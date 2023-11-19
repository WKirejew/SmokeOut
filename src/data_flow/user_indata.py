import datetime as dt

import os
import airflow
import requests as r
import requests.exceptions as rex
from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook

import ipynb.fs.full.indata_pro_ops
from ipynb.fs.full.indata_pro_ops import InData
import ipynb.fs.full.inApp_data_saving
from ipynb.fs.full.inApp_data_saving import User_Registration

# Global constants with connections of airflow
AZURE_BLOB = "azure_blob_conn"
SQL_DATABASE = "sql_database"

# Global variables
filenames =[]

# =========================================================================
# Initialization of a dag
uid_dag = DAG(
    dag_id = "process_user_indata",
    start_date = dt.datetime(2023, 11, 20, 2, 0),
    schedule_interval = "@daily",
)

# ------------------------------------------------------------------------
# -------------                 TASK 1               ---------------------
# First operation is accessing AFS and downloading list of blobs
# for accesing AFS - WasbHook is beeing used:
def _read():
    azure = WasbHook(wasb_conn_id=AZURE_BLOB)
    list = azure.get_blobs_list(container_name="jsons")
    for filename in list:
         filenames.append(filename)
    return filenames

read_AFS = PythonOperator(
    task_id = "function",
    python_callable = _read,
    dag = uid_dag
)
# ------------------------------------------------------------------------
# -------------                 TASK 2               ---------------------
# To process each of new datafiles separately, TaskGroup is introduced
with TaskGroup("indata_files_processing_task_group") as processing_group:
        for filename in filenames:
             
            @task(task_id="process_file_{0}".format(filename))
            def upload_to_azure_blob(filename: str, date: str) -> None:
                # Instantiate the connection
                azure = WasbHook(wasb_conn_id=AZURE_BLOB)
                # Set a path to download the json files
                try:
                    local_path = "assets/jsons/"
                    os.mkdir(local_path)
                except:
                    print("Folder already exists. Proceeding to download")
                # Make request to download file from Azure Blob Storage
                azure.get_file(file_path=local_path, container_name="jsons",blob_name=filename)
                # Process the file:
                file = InData("{}{}".format(local_path, filename))
                file.extract()
                User_Registration(file)
                

                # Take string, upload to S3 using predefined method
                azure.load_string(string_data=res.text, container_name="covid-data", blob_name=filename)

        upload_to_azure_blob(endpoint=endpoint, date=date)
# ------------------------------------------------------------------------
# -------------                 TASK 3               ---------------------
# Next operation is to move processed datafiles into 
# "historic_data" directory
def _move():
    print("Something")

move_files = PythonOperator(
    task_id = "function",
    python_callable = _move,
    dag = uid_dag
)

# =======================================================================
# ================              ORDER              ======================
read_AFS >> processing_group >> move_files




#Way of using PythonOperator with function
def _function():
    print("Something")

function = PythonOperator(
    task_id = "function",
    python_callable = _function,
    dag = uid_dag
)