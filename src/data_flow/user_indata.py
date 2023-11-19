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
from ipynb.fs.full.inApp_data_saving import User_Registration, InData_save

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
         filename = str.replace(filename, "/", "+")
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
            def process_file(file: str) -> None:
                # Instantiate the connections
                azure = WasbHook(wasb_conn_id=AZURE_BLOB)
                sqldb = MsSqlHook(mssql_conn_id=SQL_DATABASE)
                engine = sqldb.get_sqlalchemy_engine()
                # Set a path to download the json files
                try:
                    local_path = "assets/jsons/"
                    os.mkdir(local_path)
                except:
                    print("Folder already exists. Proceeding to download")
                # Make request to download file from Azure Blob Storage
                azure.get_file(file_path=local_path, container_name="jsons",blob_name=filename)
                # Process the file:
                local_file = InData("{}{}".format(local_path, file))
                local_file.extract()
                User_Registration(local_file)
                InData_save(local_file, engine)

            process_file(file=filename)
# ------------------------------------------------------------------------
# -------------                 TASK 3               ---------------------
# Next operation is to move processed datafiles into 
# "historic_data" directory
with TaskGroup("indata_files_processing_task_group") as move_files:
        for filename in filenames:
             
            @task(task_id="move_file_{0}".format(filename))
            def move_file(file: str) -> None:
                # Instantiate the connections
                azure = WasbHook(wasb_conn_id=AZURE_BLOB)
                # Upload the file from local storage into cloud
                local_path = "assets/jsons/"
                lf = "{}{}".format(local_path, file)
                with open(lf) as file:
                    data = file.read()
                azure.upload(container_name="historical-json", blob_name=str.replace(filename,"+","/"),data=data,blob_type="BlockBlob")
                azure.delete_file(container_name="jsons", blob_name=str.replace(filename,"+","/"), ignore_if_missing=True)

            move_file(file=filename)
# =======================================================================
# ================              ORDER              ======================
read_AFS >> processing_group >> move_files