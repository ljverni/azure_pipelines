
from datetime import datetime as dt
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import traceback
from dotenv import load_dotenv
load_dotenv()

class AzureBlobHandler:
    
    def __init__(self, account_url, container, path=None):
        self.default_credential = DefaultAzureCredential()                                       
        self.account_url = account_url
        self.container = container
        self.path = path
        self.blob_service_client = BlobServiceClient(account_url, credential=self.default_credential)  
        self.container_client = self.blob_service_client.get_container_client(container=self.container)

    ########################################

    def load_blob(self, file_path, file_content, file_format):
    
        try:
            source_path = file_path.split('/')[0]
            last_batch_no = self.get_last_batch_no()
            new_batch_no = 'batch' + str(int(last_batch_no) + 1)
            path = file_path + '_' + new_batch_no + '.' + file_format
    
            # Create a blob client using the local file name as the name for the blob
            blob_client = self.blob_service_client.get_blob_client(container=self.container, blob=f'{path}')
            blob_client.upload_blob(file_content)
            print('File loaded')
            new_batch_no = new_batch_no.split('batch')[-1]
            return new_batch_no
        
        except Exception as ex:
            print(traceback.format_exc())
    
    #########################################
    
    def change_directory(self, old_path, new_directory):
        
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container, blob=old_path)
            blob_name = blob_client.blob_name
            container_name = blob_client.container_name
            old_directory = blob_name.split('/')[-2]
            
            if old_directory != new_directory:
                new_blob_name = blob_name.replace(old_directory, new_directory)
                new_blob_client = self.blob_service_client.get_blob_client(container_name, new_blob_name)
                new_blob_client.start_copy_from_url(blob_client.url)
                blob_client.delete_blob()
       
        except Exception as ex:
            print(traceback.format_exc())

    
    ########################################
    
    def get_last_batch_no(self):
        try:
            print('Getting last batch')
                                                                                                
            # Download the blob to a local file
            last_batch_nos = sorted([int(blob.name.split('batch')[1].split('.')[0]) for blob in self.container_client.list_blobs(self.path)])
            if len(last_batch_nos) == 0:
                return '0'
            else:
                return str(max(last_batch_nos))
        except Exception as ex:
            print(traceback.format_exc())

        
