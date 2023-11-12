from indata_pro_ops import InData
import sqlalchemy as db
from sqlalchemy import inspect
import pandas as pd
import time

def User_Registration(InData):
     """
        Checks if username of InData object exists and if not, creating a query that saves the username 
        as a new user in the `user` Table with a first switch/open time as `StartTime`

        Parameters
        ----------
        InData : InData object
            An object created from .json file sended from the mobile App
        """
     mode = input("To choose local database press 'l', for online press 'o'")
     while mode != 'l' and mode != 'o':
         print("Error! Try again!")
         mode = input("To choose local database press 'l', for online press 'o'")
    # In SQLAlchemy (SQL module to work with pandas) to start connection
q   # first step is to create engine:
    # -----------------------------------------------------------------
     if mode = 'l':
        # For that although, the connection string is needed
         conn_str = ''
        # To connect to local database we need: user, password, port
        # and name of database:
         USR = input("Username:")
         PWD = input("Password:")
         PORT = '3306'
         DB = 'smokeout'
         SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost:{}/{}'.format(USR, PWD, PORT, DB)
         engine = db.create_engine(conn_str)
     else:
        # For that although, the connection string is needed
         connAzure = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:smokeout.database.windows.net,1433;Database=SmokeOut_users;Uid=Krwawe;Pwd="+input("Password")+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        # To connect to Azure database we need a prefix
         conn_str = f'mssql+pyodbc:///?odbc_connect={connAzure}'
         engine = db.create_engine(conn_str) 
    # ===================================================================
    # Extracting the metadata (needed to access the tables)
     metadata = db.MetaData()
    # Accessing `user` table of connected database 
     user = db.Table('user', metadata, autoload=True, autoload_with=engine)
    # ====================================================================
    # Checking if username is already in database and if it is not
    # inserting it in a new row of `user` table
     chkusr = False if conn.execute(db.select(user).where(user.c.username == test1.username)) is not None else True
     try:
         start = 1/chkusr
         query = user.insert.values(username=test1.username)
         exe = conn.execute(query)
     except:
         print("username already in database")