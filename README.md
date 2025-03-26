# imms_fhir_api_automation
Behave Automation for Immunisation FHIR API

# Need to check in case any other libraries to be added

Install Libraries
---------------------------------------------------
1. pip install requests
2. pip install git+https://github.com/behave/behave
3. pip install allure-behave
4. npm install papaparse

Reporting
-----------------------------------------------------
To create the json report - 
    pip install allure-behave

Command - 
    behave -f allure_behave.formatter:AllureFormatter -o output/allure-results

To convert the json file to html in Allure Reporting
----------------------------------------------------
Dwnload the latest release allure-2.32.2.zip Allure Package from https://github.com/allure-framework/allure2/releases
Unzip the folder and add the bin directory to system variable path

Command to convert the json reports to html - 
    allure serve output/allure-results

Command to generate the html report manually if BROWSE does not work - 
allure generate output/allure-results -o output/allure-report

To Open the index.html file
----------------------------------------------------
cd /output/allure-report
python3 -m http.server 8000

CSV file
----------------------------------------------------
 To read the csv file in tabular format or edit download a plugin in vscode - Edit CSV 

