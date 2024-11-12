param (
    [Parameter(mandatory=$true)]
    [string]$businessService ,
    [Parameter(mandatory=$true)]
    [string]$shortDescription,
    [Parameter(mandatory=$true)]
    [string]$assignmentGroup,
    [Parameter(mandatory=$true)]
    [string]$category,
    [Parameter(mandatory=$true)]
    [string]$callerId,
    [Parameter(mandatory=$true)]
    [string]$jobName
)

# Load config
. .\config.ps1

# Build auth header
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $user, $password)))

# Set proper headers
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add('Authorization',('Basic {0}' -f $base64AuthInfo))
$headers.Add('Accept','application/json')
$headers.Add('Content-Type','application/json')

# Specify endpoint uri
$uri_base = "https://$instance.service-now.com/api/now/table/incident"

# Check if a ticket already exists for the job name and is not closed
$uri_query = "?sysparm_query=closed_atISEMPTY%5E$vtom_job_name_field%3D$jobName&sysparm_fields=number,sys_id"
$uri_full = "$uri_base$uri_query"

$response = Invoke-RestMethod -Headers $headers -Method "get" -Uri $uri_full

$ticketNumber = ""
$ticketSysId = ""

if ($response.result.Count -eq 0) {  # Check if the result array is empty
    Write-Host "No ticket is opened for the job name specified. New ticket will be created."    
} else {
    $ticketNumber = $response.result[0].number  # Extract the value of number
    Write-Host "Ticket $ticketNumber is already opened for the job name specified. Adding child ticket."
    $ticketSysId = $response.result[0].sys_id  # Extract the value of sys_id
}

###########################
# Open a new ticket
###########################
$body = @{
    "caller_id" = $callerId
    "business_service" = $businessService
    "category" = $category
    "short_description" = $shortDescription
    "assignment_group" = $assignmentGroup
    "parent_incident" = $ticketSysId
    $vtom_job_name_field = $jobName
} | ConvertTo-Json

# Send HTTP request
$response = Invoke-RestMethod -Headers $headers -Method "post" -Uri $uri_base -Body $body

# Print response
Write-Host ("Ticket {0} created." -f $response.result.number)