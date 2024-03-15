import os
from datetime import datetime as dt
from datetime import timedelta
from azure_vault import get_secret
import msal
import requests
import csv
import base64

##########################################################################

class Email:
    
    def __init__(self, user_id_secret_name):
        self.tenant_id = get_secret('CaratacoDataGraphTenantID')
        self.authority = f"https://login.microsoftonline.com/{get_secret('CaratacoDataGraphTenantID')}"
        self.app_id = get_secret('CaratacoDataGraphAppID')
        self.scope = ["https://graph.microsoft.com/.default"]
        self.secret = get_secret('CaratacoDataGraphSecret')
        self.user_id = get_secret(user_id_secret_name)
        self.endpoint_send_message = f"https://graph.microsoft.com/v1.0/users/{self.user_id}/sendMail"
        self.endpoint_get_messages = f"https://graph.microsoft.com/v1.0/users/{self.user_id}/mailFolders/Inbox/messages"
        self.token = None
        self.email_objects = []
        self.email_attachments = []

    def get_token(self): 
        
        # Get token
        app = msal.ConfidentialClientApplication(self.app_id, authority=self.authority, client_credential=self.secret)

        # Check for token in MSAL cache
        result = app.acquire_token_silent(self.scope, account=None)

        # Request token from microsoft
        if not result:
        # print("No suitable token in cache. Get new one.")
            result = app.acquire_token_for_client(scopes=self.scope)


        # Get token
        if "access_token" in result:
            token = 'Bearer ' + result['access_token']
            self.token = token

        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))
            raise Exception("Could not retrieve token")

    ###############################################

    def send_message(self, subject, body_content):
        self.get_token()

        headers = {'Authorization': self.token}

        # Email message
        email_msg = {'Message': {'Subject': subject,
        'Body': {'ContentType': 'Text', 'Content': body_content},
        'ToRecipients': [{'EmailAddress': {'Address': 'lucianoverni@gmail.com'}}]
        },
        'SaveToSentItems': 'true'}

        # Send Email
        response = requests.post(self.endpoint_send_message, headers=headers, json=email_msg)
        
        if response.ok:
            print('Sent email alert successfully')
        else:
            print(response.json())

    ###############################################

    def get_messages(self, subject=None, last_days=None, start_date=None, end_date=None):
        email_ids = []
        params_string = f'''hasAttachments eq true and '''

        if last_days == None and start_date == None:
            raise Exception('To get message, either last_days or start_date must be passed')
        
        if last_days:
            if type(last_days) != int:
                raise Exception('Last days must be integer')
            else:
                start_date_str = (dt.today() - timedelta(last_days)).strftime('%Y-%m-%dT00:00:00Z')
                end_date_str = dt.today().strftime('%Y-%m-%dT23:59:59Z')
                params_string += f"receivedDateTime ge {start_date_str} and receivedDateTime le {end_date_str} "

        if start_date != None and end_date != None:
            params_string += f"receivedDateTime ge {start_date} and receivedDateTime le {end_date} "

        if subject != None:
           params_string += f"and subject eq '{subject}'"
       
        self.get_token()
        headers = {'Authorization': self.token}

        params = {'$filter': params_string}

        # Send Email
        response = requests.get(self.endpoint_get_messages, headers=headers, params=params)
        if response.ok:
            for email in response.json()['value']:
                self.email_objects.append(email)

        else:
            print(response.url)
            print(response.json())


   ###############################################                                             
                                                                                               
    def get_attachments(self, subject=None, last_days=None, start_date=None, end_date=None):
        self.get_messages(subject, last_days, start_date, end_date)
        email_objects = self.email_objects
        self.get_token()
        headers = {'Authorization': self.token}
       
        for email in email_objects:
            email_id = email['id']
            sender = email['sender']['emailAddress']['address']
            received_date = email['receivedDateTime']

            endpoint_attachment_list = f"https://graph.microsoft.com/v1.0/users/{self.user_id}/messages/{email_id}/attachments"
       
            response = requests.get(endpoint_attachment_list, headers=headers)
            
            if response.ok:
                for attachment in response.json()['value']:
                    attachment_dict = {}
                    attachment_id = attachment['id']
                    
                    endpoint_get_attachment = f"https://graph.microsoft.com/v1.0/users/{self.user_id}/messages/{email_id}/attachments/{attachment_id}"

                    response = requests.get(endpoint_get_attachment, headers=headers)
                    json_response = response.json()
                    attachment_dict['sender'] = sender
                    attachment_dict['received_date'] = received_date
                    attachment_dict['attachment_name'] = json_response['name']
                    attachment_dict['attachment_content'] = json_response['contentBytes']
                    self.email_attachments.append(attachment_dict)

            else:
                print(response.url)
                print(response.json())
        
        return self.email_attachments
