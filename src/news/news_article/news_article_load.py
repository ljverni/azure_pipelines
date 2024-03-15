import requests
import json
import os
import pandas as pd
from datetime import datetime as dt
from src.utilities.azure_blob import AzureBlobHandler
from src.utilities.dw_connect_prod import connect
import pyodbc
from src.utilities.logger import Log
import time
import traceback

# log = Log(os.path.abspath(__file__), time.time())

def load_files(file_name, file_content):
    cnx = connect()
    cursor = cnx.cursor() 
    row_count = len(file_content)
    batch_no = file_name.split('batch')[-1].split('.')[0]
    
    for row in file_content:
        cursor.execute('''INSERT INTO news.news_article_src (article_id, title, link, content, publication_date, source_id, source_country, article_language, source_file_name, batch_no) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', row['article_id'], row['title'], row['link'], row['content'], row['pubDate'], row['source_id'], str(row['country']), row['language'], file_name, batch_no)
        cnx.commit()
    
    cnx.close()
    
    return row_count, batch_no

#####################################################

def get_files(account_url, container, entity):
    
    blob_handler = AzureBlobHandler(account_url, container, entity)
    
    path_not_loaded = blob_handler.path + '/notloaded' 
        
    blob_list = blob_handler.container_client.list_blobs(path_not_loaded)
    blob_files = {}
    for blob in blob_list:
        blob_name = blob['name']
    
        file_content = json.loads(blob_handler.container_client.download_blob(blob_name).read())
        
        blob_files[blob_name] = file_content
       
    return blob_files

#####################################################

def change_blob_directory(account_url, container, entity, file_name):
    blob_handler = AzureBlobHandler(account_url, container, entity)
    blob_handler.change_directory(file_name, 'loaded') 

#####################################################

container_details = {
        'account_url': 'https://caratacoblob1.blob.core.windows.net',
        'container': 'prod',
        'entity': 'news_articles',
        'file_format': 'json'
        }


if __name__ == '__main__':
    account_url = container_details['account_url']
    container = container_details['container']
    entity = container_details['entity']
    file_format = container_details['file_format']

    try:
        files = get_files(account_url, container, entity)

        for file_name in files:
            if container_details['file_format'] in file_name:
                file_content = files[file_name]
                row_count, batch_no = load_files(file_name, file_content)
                change_blob_directory(account_url, container, entity, file_name)
                # log.log_success(row_count, batch_no)
        print('DW load success')
    
    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        # log.log_error(ex)
