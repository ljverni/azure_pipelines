import pyodbc
import os
import csv
from datetime import datetime as dt
from datetime import timedelta
import os
import dw_connect_prod
import time
import traceback
from dotenv import load_dotenv
load_dotenv()

######################################################

def read_log(path):
    row_lst = []
        
    with open(path, encoding='utf8') as file:
        csvreader = csv.reader(file) 
                     
        for row in csvreader:
            if row not in row_lst:
                row_lst.append(row)
    
    return row_lst
    
######################################################################

def load_log():
    for stage in ['extract', 'load']:
        path = os.path.expanduser('~') + f'/projects/pipelines/{stage}/log/{stage}.log'
        try:
            cnx = dw_connect_prod.connect()
            cursor = cnx.cursor()
        
            for row in read_log(path):
                execution_date = row[0:1]
                script_path = row[2:3]
                values = tuple(execution_date + script_path + row)
                
                insert = """
                IF NOT EXISTS(SELECT * FROM audit.etl_log WHERE execution_date = ? AND script_path = ?)
                BEGIN
                  INSERT INTO audit.etl_log (execution_date, elapsed_time, script_path, log_level, msg, row_count, batch_no) VALUES (?, ?, ?, ?, ?, ?, ?)
                END;
                """
                cursor.execute(insert, values)
                cnx.commit()
            
            
        except Exception as e:
            print(traceback.format_exc())

            cnx.close()
            quit()
    
    cnx.close()

load_log()
