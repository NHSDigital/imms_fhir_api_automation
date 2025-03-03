# imms_fhir_api_automation
Behave Automation for Immunisation FHIR API

Install Libraries
---------------------------------------------------
1. pip install requests
2. pip install git+https://github.com/behave/behave
3. pip install allure-behave
4. 

Reporting
-----------------------------------------------------
1. To create the json report - 
    pip install allure-behave

Command - 
    behave -f allure_behave.formatter:AllureFormatter -o FolderNameWhereReportWillBeSaved

To convert the json file to html in Allure Reporting
----------------------------------------------------
2. Dwnload the latest release allure-2.32.2.zip Allure Package from https://github.com/allure-framework/allure2/releases
   Unzip the folder and add the bin directory to system variable path

 Command to convert the json reports to html - 
    allure serve FolderNameWhereReportIsSaved

CSV file
----------------------------------------------------
 To read the csv file in tabular format or edit download a plugin in vscode - Edit CSV 