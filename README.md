# Visual TOM ServiceNow Integration
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.md)&nbsp;
[![fr](https://img.shields.io/badge/lang-fr-yellow.svg)](README-fr.md)  

This project provides scripts to create and manage ServiceNow tickets from Visual TOM.
To avoid too many tickets, the script checks if a ticket already exists for the object name and is not closed.
If it does, it will create a child ticket with the new information.
If not, it will create a new ticket.

# Disclaimer
No Support and No Warranty are provided by Absyss SAS for this project and related material. The use of this project's files is at your own risk.

Absyss SAS assumes no liability for damage caused by the usage of any of the files offered here via this Github repository.

Consultings days can be requested to help for the implementation.

# Prerequisites

  * Visual TOM 7.1.2 or greater
  * ServiceNow instance with REST API enabled
  * Custom field in ServiceNow to store the Visual TOM object name (Jobs, Applications, Agents, etc.)

# Instructions

The script can be customized to fit your needs for the ServiceNow fields. You can find the fields in the REST API explorer of your ServiceNow instance ([[https://YOUR-INSTANCE.service-now.com/now/nav/ui/classic/params/target/%24restapi.do]]).

You can choose between the PowerShell script or the Python script depending on your environment.

### PowerShell Script
1. Edit the config.ps1 file with your ServiceNow credentials and specific field names
2. Create an alarm in Visual TOM to trigger the script (example below for a job to be adapted)
  ```powershell
  powershell.exe -file FULL_PATH_TO_SCRIPT\ServiceNow_CreateTicket.ps1 -businessService "My Service" -shortDescription "Job has failed" -assignmentGroup "SAP L2" -category "1F Other Unknown Bugs / Errors" -callerId "charles.beckley@example.com" -objectName "{VT_FULL_JOBNAME}"
  ```

### Python Script
1. Edit the config.py file with your ServiceNow credentials and specific field names
2. Create an alarm in Visual TOM to trigger the script (example below for a job to be adapted)
  ```python
  python FULL_PATH_TO_SCRIPT/ServiceNow_CreateTicket.py -businessService "My Service" -shortDescription "Job has failed" -assignmentGroup "SAP L2" -category "1F Other Unknown Bugs / Errors" -callerId "charles.beckley@example.com" -objectName "{VT_FULL_JOBNAME}"
  ```

# License
This project is licensed under the Apache 2.0 License - see the [LICENSE](license) file for details


# Code of Conduct
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS has adopted the [Contributor Covenant](CODE_OF_CONDUCT.md) as its Code of Conduct, and we expect project participants to adhere to it. Please read the [full text](CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.
