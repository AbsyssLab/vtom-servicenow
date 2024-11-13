import requests
import json
import argparse

from config import *

# Parse arguments
parser = argparse.ArgumentParser(description='Create a ServiceNow ticket')
parser.add_argument('--businessService', required=True, help='Business service name')
parser.add_argument('--shortDescription', required=True, help='Short description of the issue')
parser.add_argument('--assignmentGroup', required=True, help='Assignment group name')
parser.add_argument('--category', required=True, help='Category of the issue')
parser.add_argument('--callerId', required=True, help='Caller ID')
parser.add_argument('--objectName', required=True, help='Object name')
args = parser.parse_args()

# Set proper headers
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Specify endpoint uri
uri_base = f"https://{instance}.service-now.com/api/now/table/incident"

# Check if a ticket already exists for the object and is not closed
uri_query = f"?sysparm_query=closed_atISEMPTY^{vtom_object_name_field}={args.objectName}&sysparm_fields=number,sys_id"

response = requests.get(uri_base + uri_query, headers=headers, auth=(user, password))
if response.status_code != 200:
    print(f"Error: {response.status_code} - {response.text}")
    exit(1)
ticket_number = ""
ticket_sys_id = ""

if len(response.json()['result']) == 0:  # Check if the result array is empty
    print(f"No ticket is opened for the object {args.objectName} specified. New ticket will be created.")    
else:
    ticket_number = response.json()['result'][0]['number']  # Extract the number of the ticket
    print(f"Ticket {ticket_number} is already opened for the object {args.objectName} specified. Adding child ticket.")
    ticket_sys_id = response.json()['result'][0]['sys_id']  # Extract the sys_id of the ticket to link the child ticket to the parent ticket

###########################
# Open a new ticket
###########################
body = {
    "caller_id": args.callerId,
    "business_service": args.businessService,
    "category": args.category,
    "short_description": args.shortDescription,
    "assignment_group": args.assignmentGroup,
    "parent_incident": ticket_sys_id,
    vtom_object_name_field: args.objectName
}

# Send HTTP request
response = requests.post(uri_base, headers=headers, json=body, auth=(user, password))
if response.status_code not in [200, 201]:
    print(f"Error: {response.status_code} - {response.text}")
    exit(1)

# Print response
print(f"Ticket {response.json()['result']['number']} created.")