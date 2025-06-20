# imms_fhir_api_automation

Behave Automation for Immunisation FHIR API

## Need to check in case any other libraries to be added

## Installation

This test pack requires Python 3.10 installed on the system or greater to run.

To execute the tests from your system, please follow the 4 easy steps below:

1. Clone the repo to any local folder
2. Create a virtual environment

    ```console
    # python -m venv .venv
    ```

3. Install all dependencies

    ```console
    # pip install -r .\requirements.txt
    ```

4. in git bash terminal

    ```console
    source .venv/Scripts/activate
    ```

5. in Terminal

    ```console
        .venv\Scripts\Activate.ps1

    ```

6. Need to create .env file, please get in touch with Imms FHIR API Test team to get the content of the file

7. run following command to see that test are discovered

     ```console
        # pytest --collect-only
     ```

8. install and configure Aws CLI using following commands:
   1. pip install awscli
   2. aws configure

----DO NOT USE BELOW---------------------------------------------

Reporting
-----------------------------------------------------

To create the json report -
    pip install allure-behave

Command -
    behave -f allure_behave.formatter:AllureFormatter -o output/allure-results

To convert the json file to html in Allure Reporting
----------------------------------------------------

Dwnload the latest release allure-2.32.2.zip Allure Package from <https://github.com/allure-framework/allure2/releases>
Unzip the folder and add the bin directory to system variable path

Command to convert the json reports to html -
    allure serve output/allure-results

Command to generate the html report manually if BROWSE does not work -
allure generate output/allure-results -o output/allure-report --clean

Start a http server to view the results -
python -m http.server

To Open the index.html file
----------------------------------------------------

cd output/allure-report
python3 -m http.server 8000

CSV file
----------------------------------------------------

 To read the csv file in tabular format or edit download a plugin in vscode - Edit CSV
