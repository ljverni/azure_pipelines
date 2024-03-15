from dotenv import load_dotenv
import os
import pyodbc
load_dotenv()

def connect():
    server = 'caratacodwsvr.database.windows.net'
    database = 'caratacodw'
    driver = '{odbc driver 18 for sql server}'
    client_id = os.environ.get('AZURE_CLIENT_ID')
    client_secret = os.environ.get('AZURE_CLIENT_SECRET')
    
    if client_id and client_secret:
        cnx = pyodbc.connect('driver='+driver+';server=tcp:'+server+';port=1433;database='+database+';UID='+client_id+';PWD='+client_secret+';authentication=ActiveDirectoryServicePrincipal;Encrypt=yes;')
    else:
        cnx = pyodbc.connect('driver='+driver+';server=tcp:'+server+';port=1433;database='+database+';authentication=ActiveDirectoryMsi')

    return cnx
