# SmokeOut

Incubated in 2022 start-up of a mechatronical device connected with mobile app for tobacco addicts, 
aiming at cesseting and monitoring problematic behaviours during their road to full recovery.
Thanks to author of the idea [Bartek Kubrak](https://www.linkedin.com/in/bartosz-kubrak-6659951a1/)
and general technnological engineer [Konrad Sejud](https://www.linkedin.com/in/konrad-sejud-57461a27b/)

## Requirements:

### Apache airflow:
Typical installation of [apache-airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html)

Providers: [installation by *pip install (**provider**)*]
> apache-airflow-providers-microsoft-azure \
> apache-airflow-providers-microsoft-mssql

**Establishing approperiate connections:**

[Azure Blob Storage using wasb Hook](https://docs.astronomer.io/learn/connections/azure-blob-storage) \
[Microsoft SQL at Azure](https://docs.astronomer.io/learn/connections/ms-sqlserver)


### Drivers:
[ODBC Driver for SQL Server](https://go.microsoft.com/fwlink/?linkid=2249006)

### Python Libraries:
> pandas \
> fastapi \
> uvicorn[standard] \
> pydantic \
> azure-identity \
> azure-storage-blob \
> mysqlclient (for testing in mysql) \
> SQLAlchemy \
> ipynb (to import files from notebooks)

###  Generating inputs:

## Using the project:

For purpose of writing new data into SQL database permission, contact: 
> wojtasss99@gmail.com

For read only:

DataBase looks like this:
![db](/assets/images/SmokeOutDB.png)
