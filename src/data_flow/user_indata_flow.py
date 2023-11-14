import json
import datetime as dt

import airflow
import requests as r
import requests.exceptions as rex
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import ipynb.fs.full.indata_pro_ops
import ipynb.fs.full.inApp_data_saving

uid_dag = DAG(
    dag_id = "save_user_indata",
    start_date = dt.datetime(2023, 11, 1, 2, 0),
    schedule_interval = "@daily",
)
#Loading the .json with input data


#Way of using PythonOperator with function
def _function():
    print("Something")

function = PythonOperator(
    task_id = "function",
    python_callable = _function,
    dag = uid_dag
)