param (
    [Parameter(mandatory=$false)]
    [string]$businessService ,
    [Parameter(mandatory=$true)]
    [string]$shortDescription,
    [Parameter(mandatory=$false)]
    [string]$assignmentGroup,
    [Parameter(mandatory=$false)]
    [string]$category,
    [Parameter(mandatory=$true)]
    [string]$callerId,
    [Parameter(mandatory=$true)]
    [string]$objectName,
    [Parameter(mandatory=$false)]
    [string]$outAttachmentFile,
    [Parameter(mandatory=$false)]
    [string]$outAttachmentName,
    [Parameter(mandatory=$false)]
    [string]$errorAttachmentFile,
    [Parameter(mandatory=$false)]
    [string]$errorAttachmentName
)

if ($PSBoundParameters.ContainsKey('outAttachmentFile') -and -not $PSBoundParameters.ContainsKey('outAttachmentName') -or -not $PSBoundParameters.ContainsKey('outAttachmentFile') -and $PSBoundParameters.ContainsKey('outAttachmentName')) {
    Write-Host "Error: -outAttachmentName is required when -outAttachmentFile is specified."
    exit
}
if ($PSBoundParameters.ContainsKey('errorAttachmentFile') -and -not $PSBoundParameters.ContainsKey('errorAttachmentName') -or -not $PSBoundParameters.ContainsKey('errorAttachmentFile') -and $PSBoundParameters.ContainsKey('errorAttachmentName')) {
    Write-Host "Error: -errorAttachmentName is required when -errorAttachmentFile is specified."
    exit
}

# Load config
# Change to script folder
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

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

# Check if a ticket already exists for the object and is not closed
$uri_query = "?sysparm_query=closed_atISEMPTY%5E$vtom_object_name_field%3D$objectName&sysparm_fields=number,sys_id"
$uri_full = "$uri_base$uri_query"
try {
    $response = Invoke-RestMethod -Headers $headers -Method "get" -Uri $uri_full
} catch {
    Write-Host "HTTP request failed with status code: " $_.Exception.Response.StatusCode.Value__
    Write-Host "Response: " $_.Exception.Response
    exit
}

$ticketNumber = ""
$ticketSysId = ""

if ($response.result.Count -eq 0) {  # Check if the result array is empty
    Write-Host ("No ticket is opened for the object {0} specified. New ticket will be created." -f $objectName)    
} else {
    $ticketNumber = $response.result[0].number  # Extract the number of the ticket
    Write-Host ("Ticket {0} is already opened for the object {1}. Adding child ticket." -f $ticketNumber, $objectName)
    $ticketSysId = $response.result[0].sys_id  # Extract the value of sys_id to link the child ticket to the parent ticket
}

###########################
# Open a new ticket
###########################
# The body can be updated to add more fields depending on the needs
$body = @{
    "caller_id" = $callerId
    "business_service" = $businessService
    "category" = $category
    "short_description" = $shortDescription
    "assignment_group" = $assignmentGroup
    "parent_incident" = $ticketSysId
    $vtom_object_name_field = $objectName
} | ConvertTo-Json

# Send HTTP request
try {
    $response = Invoke-RestMethod -Headers $headers -Method "post" -Uri $uri_base -Body $body
} catch {
    Write-Host "HTTP request failed with status code: " $_.Exception.Response.StatusCode.Value__
    Write-Host "Response: " $_.Exception.Response
    exit
}

# Print response
Write-Host ("Ticket {0} created." -f $response.result.number)

###########################
# Add attachments
###########################
$headers['Content-Type'] = 'image/jpeg'
$sys_id = $response.result.sys_id
$ticketNumber = $response.result.number

if ($outAttachmentFile -ne "") {
    # Check if the file exists
    if (-not (Test-Path $outAttachmentFile)) {
        Write-Host "Error: File $outAttachmentFile does not exist."
        exit
    }
    
    # Check if the file is empty
    if ((Get-Item $outAttachmentFile).Length -eq 0) {
        Write-Host "Info: Output log file is empty. Skipping attachment."
    } else {
        try {
            $uri_full = "https://$instance.service-now.com/api/now/attachment/file?table_name=incident&table_sys_id=$sys_id&file_name=$($outAttachmentName).log"
            $body = Get-Content -Path $outAttachmentFile -Raw
            $response = Invoke-RestMethod -Headers $headers -Method "post" -Uri $uri_full -Body $body
            Write-Host "Ticket $ticketNumber updated with attachment $($outAttachmentName).log."
        } catch {
            Write-Host "HTTP request failed with status code: " $_.Exception.Response.StatusCode.Value__
            Write-Host "Response: " $_.Exception
            exit
        }
    }
}

if ($errorAttachmentFile -ne "") {  # Add error attachment if specified
    # Check if the file exists
    if (-not (Test-Path $errorAttachmentFile)) {
        Write-Host "Error: File $errorAttachmentFile does not exist."
        exit
    }
    
    # Check if the file is empty
    if ((Get-Item $errorAttachmentFile).Length -eq 0) {
        Write-Host "Info: Error log file is empty. Skipping attachment."
    } else {
        try {
            $uri_full = "https://$instance.service-now.com/api/now/attachment/file?table_name=incident&table_sys_id=$sys_id&file_name=$($errorAttachmentName).log"
            $body = Get-Content -Path $errorAttachmentFile -Raw
            $response = Invoke-RestMethod -Headers $headers -Method "post" -Uri $uri_full -Body $body
            Write-Host "Ticket $ticketNumber updated with attachment $($errorAttachmentName).log."
        } catch {
            Write-Host "HTTP request failed with status code: " $_.Exception.Response.StatusCode.Value__
            Write-Host "Response: " $_.Exception.Response
            exit
        }
    }
}
