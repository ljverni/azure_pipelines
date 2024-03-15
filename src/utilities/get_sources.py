from dotenv import load_dotenv
import os
import pyodbc
import dw_connect_prod
from dotenv import load_dotenv
load_dotenv()

def active():
    sources = []
    cnx = dw_connect_prod.connect()
    cursor = cnx.cursor() 
    
    result = cursor.execute('''SELECT table_name, source_name from audit.source WHERE active = '1' ''')
    
    for source in result:
        sources.append(source)
    
    cnx.close()

    return sources
