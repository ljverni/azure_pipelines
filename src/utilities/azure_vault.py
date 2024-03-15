
import os
import sys
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
load_dotenv()

def get_secret(secret_name):

    key_vault_name = os.environ.get('CARATACO_VAULT')
    vault_url = f'https://{key_vault_name}.vault.azure.net'
    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)


    retrieved_secret = client.get_secret(secret_name)
    
    return retrieved_secret.value

if __name__ == '__main__':
    try:
        print(get_secret(sys.argv[1]))
    except IndexError:
        print('No parameter')
