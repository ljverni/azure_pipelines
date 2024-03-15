from dotenv import load_dotenv
import os
import pyodbc
load_dotenv()

def connect():
    server = 'caratacodwsvrdev.database.windows.net'
    database = 'caratacodwdev'
    driver = '{odbc driver 18 for sql server}'
    cnx = pyodbc.connect('driver='+driver+';server=tcp:'+server+';port=1433;database='+database+';authentication=ActiveDirectoryMsi')
    return cnx

cnx = connect()
cur = cnx.cursor()

results = cur.execute('''SELECT TOP(1) date_extracted FROM source.news_article''')
print(results)
cnx.close()
