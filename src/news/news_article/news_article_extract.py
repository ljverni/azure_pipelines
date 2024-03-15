import requests
import json
from datetime import datetime as dt
from src.utilities.azure_blob import AzureBlobHandler
import os
from src.utilities.azure_vault import get_secret
from src.utilities.logger import Log
import time
import traceback

# log = Log(os.path.abspath(__file__), time.time())

def api_values():
    app_key = get_secret('NewsAPIKey')

    headers = {"apikey": app_key}
    endpoint = 'https://newsdata.io/api/1/news'
    params = {
        "apikey": app_key,
        "country": "jp",
        "language": "en"
        }
    
    return app_key, headers, endpoint, params


def extract(app_key, headers, endpoint, params):
    
    response = requests.get(endpoint, params=params, headers=headers)
    response_status = response.status_code
    
    if response_status != 200:
        raise Exception(f'Response status: {response_status}')
    else:
        json_response = response.json()
        json_results = json_response['results']
        row_count = len(json_results)
        results = json.dumps(json_results)
        return results, row_count


def load(container_details, file_content):
    account_url = container_details['account_url']
    container = container_details['container']
    entity = container_details['entity']
    file_format = container_details['file_format']

    blob_handler = AzureBlobHandler(account_url, container, entity)
    date = dt.today().strftime('%Y%m%d%H%M%S')
    file_path = f"{entity}/notloaded/{entity}_{date}"
    batch_no = blob_handler.load_blob(file_path, file_content, file_format)

    return batch_no

container_details = {
        'account_url': 'https://caratacoblob1.blob.core.windows.net',
        'container': 'prod',
        'entity': 'news_articles',
        'file_format': 'json'
        }

##############################################

if __name__ == '__main__':
    try:
        app_key, headers, endpoint, params = api_values()
        file_content, row_count = extract(app_key, headers, endpoint, params)
        batch_no = load(container_details, file_content)
        # log.log_success(row_count, batch_no)
    
    except Exception as ex:
        print(ex)
        # log.log_error(ex)

