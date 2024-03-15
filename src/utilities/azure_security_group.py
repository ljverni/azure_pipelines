
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os
import sys
from dotenv import load_dotenv
load_dotenv()

action = sys.argv[1]
subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
resource_group_name = sys.argv[2]
network_security_group_name = sys.argv[3]
security_rule_name = sys.argv[4]
if len(sys.argv) == 6:
    ip_address = sys.argv[5]

def create_inbound_ssh_rule(subscription_id, resource_group_name, network_security_group_name, security_rule_name, ip_address):
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
        )

    response = client.security_rules.begin_create_or_update(
        resource_group_name=resource_group_name,
        network_security_group_name=network_security_group_name,
        security_rule_name=security_rule_name,
        
        security_rule_parameters={
            "properties": {
                "access": "Allow",
                "destinationAddressPrefix": "*",
                "destinationPortRange": "22",
                "direction": "Inbound",
                "priority": "100",
                "protocol": "TCP",
                "sourceAddressPrefix": ip_address,
                "sourcePortRange": "*",
            }
        },
    ).result()


    print(security_rule_name, 'created successfully')

############################################

def delete_inbound_ssh_rule(subscription_id, resource_group_name, network_security_group_name, security_rule_name):
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
        )

    client.security_rules.begin_delete(
        resource_group_name=resource_group_name,
        network_security_group_name=network_security_group_name,
        security_rule_name=security_rule_name,
        ).result()

    print(security_rule_name, 'deleted successfully')



if __name__ == "__main__":
    if action == 'create':
        create_inbound_ssh_rule(subscription_id, resource_group_name, network_security_group_name, security_rule_name, ip_address)
    elif action == 'delete':
        delete_inbound_ssh_rule(subscription_id, resource_group_name, network_security_group_name, security_rule_name)
