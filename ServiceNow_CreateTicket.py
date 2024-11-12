import requests
import json
import argparse

from config import *

# Parse arguments
parser = argparse.ArgumentParser(description='Create a ServiceNow ticket')
parser.add_argument('--business-service', required=True, help='Business service name')
parser.add_argument('--short-description', required=True, help='Short description of the issue')
parser.add_argument('--assignment-group', required=True, help='Assignment group name')
parser.add_argument('--category', required=True, help='Category of the issue')
parser.add_argument('--caller-id', required=True, help='Caller ID')
parser.add_argument('--job-name', required=True, help='Job name')
args = parser.parse_args()

# Set proper headers
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Specify endpoint uri
uri_base = f"https://{instance}.service-now.com/api/now/table/incident"

# Check if a ticket already exists for the job name and is not closed
uri_query = f"?sysparm_query=closed_atISEMPTY^{vtom_job_name_field}={args.job_name}&sysparm_fields=number,sys_id"

response = requests.get(uri_base + uri_query, headers=headers, auth=(user, password))

ticket_number = ""
ticket_sys_id = ""
print(response.json())
if len(response.json()['result']) == 0:  # Check if the result array is empty
    print("No ticket is opened for the job name specified. New ticket will be created.")    
else:
    ticket_number = response.json()['result'][0]['number']  # Extract the value of number
    print(f"Ticket {ticket_number} is already opened for the job name specified. Adding child ticket.")
    ticket_sys_id = response.json()['result'][0]['sys_id']  # Extract the value of sys_id

###########################
# Open a new ticket
###########################
body = {
    "caller_id": args.caller_id,
    "business_service": args.business_service,
    "category": args.category,
    "short_description": args.short_description,
    "assignment_group": args.assignment_group,
    "parent_incident": ticket_sys_id,
    vtom_job_name_field: args.job_name
}

# Send HTTP request
response = requests.post(uri_base, headers=headers, json=body, auth=(user, password))

# Print response
print(f"Ticket {response.json()['result']['number']} created.")