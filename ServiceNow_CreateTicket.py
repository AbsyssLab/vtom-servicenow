import requests
import argparse

from config import *

# Parse arguments
parser = argparse.ArgumentParser(description='Create a ServiceNow ticket')
parser.add_argument('--businessService', required=False, help='Business service name')
parser.add_argument('--shortDescription', required=True, help='Short description of the issue')
parser.add_argument('--assignmentGroup', required=False, help='Assignment group name')
parser.add_argument('--category', required=False, help='Category of the issue')
parser.add_argument('--callerId', required=True, help='Caller ID')
parser.add_argument('--objectName', required=True, help='Object name')
parser.add_argument('--outAttachmentFile', required=False, help='Path to the output attachment file')
parser.add_argument('--outAttachmentName', required=False, help='Name of the output attachment file')
parser.add_argument('--errorAttachmentFile', required=False, help='Path to the error attachment file')
parser.add_argument('--errorAttachmentName', required=False, help='Name of the error attachment file')

args = parser.parse_args()

if args.outAttachmentFile and not args.outAttachmentName or not args.outAttachmentFile and args.outAttachmentName:
    print("Error: --outAttachmentName is required when --outAttachmentFile is specified.")
    exit(1)
if args.errorAttachmentFile and not args.errorAttachmentName or not args.errorAttachmentFile and args.errorAttachmentName:
    print("Error: --errorAttachmentName is required when --errorAttachmentFile is specified.")
    exit(1)

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
# The body can be updated to add more fields depending on the needs
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

###########################
# Add attachments
###########################
headers['Content-Type'] = 'image/jpeg'
sys_id = response.json()['result']['sys_id']
ticketNumber = response.json()['result']['number']

if args.outAttachmentFile != "":
    uri_full = f"https://{instance}.service-now.com/api/now/attachment/file?table_name=incident&table_sys_id={sys_id}&file_name={args.outAttachmentName}.log"
    with open(args.outAttachmentFile, 'rb') as file:
        body = file.read()
    response = requests.post(uri_full, headers=headers, data=body, auth=(user, password))
    if response.status_code != 201:
        print(f"Error: {response.status_code} - {response.text}")
        exit(1)
    print(f"Ticket {ticketNumber} updated with attachment {args.outAttachmentName}.log.")

if args.errorAttachmentFile != "":  # Add error attachment if specified
    uri_full = f"https://{instance}.service-now.com/api/now/attachment/file?table_name=incident&table_sys_id={sys_id}&file_name={args.errorAttachmentName}.log"
    with open(args.errorAttachmentFile, 'rb') as file:
        body = file.read()
    if body.decode() != "{VT_JOB_LOG_ERR_CONTENT}\n":     #When empty error log, the file contains the name of the variable
        response = requests.post(uri_full, headers=headers, data=body, auth=(user, password))
        if response.status_code != 201:
            print(f"Error: {response.status_code} - {response.text}")
            exit(1)
        print(f"Ticket {ticketNumber} updated with attachment {args.errorAttachmentName}.log.")
    else:
        print("No error log to attach.")
