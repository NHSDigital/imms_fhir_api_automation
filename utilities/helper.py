import csv
from datetime import datetime
import os
import shutil
from utilities.soft_assertions import SoftAssertions
from utilities.config import *
import json
import uuid
import allure
# from allure_commons.types import AttachmentType
import re


soft_assertions = SoftAssertions()
config = getConfigParser()

import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def deleteCreate(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def readJSONFileNames(search_keyword):
    read_FileName = []
    for fileName in os.listdir(config['CREATE']['InputPath']):     
        if search_keyword in fileName and fileName.endswith('.json'):
            read_FileName.append(fileName)
   
    totalFiles = len(read_FileName)
    return read_FileName, totalFiles


def updateJSONFiles(search_keyword, update_key, update_value):
    json_files = {}
    for fileName in os.listdir(config['CREATE']['InputPath']):     
        guid = str(uuid.uuid4())
        guidPath = "identifier.0.value"
        update_key = str(update_key) + "," + guidPath
        update_value = str(update_value)  + "," + guid

        updateKeys = str(update_key).split(",")
        updateValues = str(update_value).split(",")

        if search_keyword in fileName and fileName.endswith('.json'):
            filePath = config['CREATE']['InputPath'] + fileName         
            try:
                with open(filePath, 'r') as file:
                    jsonData = json.load(file)

                    for updateKey, updateValue in zip(updateKeys, updateValues):
                        temp = jsonData
                        keys = updateKey.split('.')
                        for key in keys[:-1]:
                            if key.isdigit():
                                key = int(key)
                            if isinstance(temp, list):
                                temp = temp[key]
                            else:
                                temp = temp.setdefault(key, {})
                        
                        final_key = keys[-1]
                        if final_key.isdigit() and isinstance(temp, list):
                            temp[int(final_key)] = updateValue
                        else:
                            temp[final_key] = updateValue 

                        if updateValue.lower() == "null" or updateValue == "" or updateValue.lower() == "none":
                            temp.pop(final_key, None)
            
            except Exception as e:
                print(f"Error processing file {fileName}: {e}")
    
        json_files[fileName] = jsonData    

    return json_files


def validate_json_fields(base_json, target_json, path=""):
    if isinstance(base_json, dict):
        for key in base_json:
            current_path = f"{path}.{key}" if path else key

            assert key in target_json, (f"Key '{current_path}' missing in Response JSON.")
            validate_json_fields(base_json[key], target_json[key], current_path)

    elif isinstance(base_json, list):
        assert isinstance(target_json, list), (f"Type mismatch at '{path}': Expected list but found {type(target_json).__name__}")
        # soft_assertions.assert_condition(isinstance(target_json, list), f"At '{path}': Expected list but found {type(target_json).__name__}")
        assert len(base_json) == len(target_json), (f"Mismatch at '{path}': List lengths differ ({len(base_json)} vs {len(target_json)}).")
        for index, (item1, item2) in enumerate(zip(base_json, target_json)):
          validate_json_fields(item1, item2, path + f"[{index}]")

    else:
        try:
            with allure.step(f"Validating field: {path}"):
                if isinstance(base_json, re.Pattern):
                    soft_assertions.assert_condition(bool(re.match(base_json, target_json)), f"{path}: Expected guid pattern, Found {target_json}")
                # if base_json in r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$" 
                else:
                    # assert base_json == target_json,(f"Mismatch at '{path}': Expected {base_json}, Found {target_json}")
                    soft_assertions.assert_condition(base_json == target_json, f"{path}: Expected {base_json}, Found {target_json}")
                    
        except AssertionError as e:
            print(e)


def operationOutcomeResJson(code, diagnostics):
    profile = config['OPERATIONOUTCOME']['profile']
    system = config['OPERATIONOUTCOME']['system']

    response = {
        # "resourceType": "OperationOutcome",
        # "id": "faf54470-2a91-40e8-9b33-5751fcfa3668",
        "meta": {
            "profile": [
                profile
            ]
        },
        "issue": [
            {
                "severity": "error",
                "code": code.lower(),
                "details": {
                    "coding": [
                        {
                            "system": system,
                            "code": code.upper(),
                        }
                    ]
                },
                "diagnostics": diagnostics
            }
        ]
    }
        
    return json.dumps(response)


def format_timestamp(timestamp):
    parts = timestamp.split(".")

    if len(parts) == 2:
        milliseconds, timezone = parts[1].split("+")
        milliseconds = milliseconds.ljust(6, "0")
        
        return f"{parts[0]}.{milliseconds}+{timezone}"


# def capture_screenshot_on_failure(driver):
#     screenshot_path = "screenshot_failure.png"
#     driver.save_screenshot(screenshot_path)

#     with open(screenshot_path, "rb") as screenshot_file:
#         allure.attach(screenshot_file.read(), name="Failure Screenshot", attachment_type=AttachmentType.PNG)



def readInputCSV_search():
    with open('input_csv_files/searchParams.csv') as searchCSV:
        searchReader = csv.reader(searchCSV,delimiter=',')

        for row in searchReader:
            print(row)

def covert_to_expected_date_format(date_string):
    try:
        dt = datetime.fromisoformat(date_string.replace("+00:00", ""))
        formatted_dt = dt.isoformat(timespec="microseconds") + "+00:00"
        return formatted_dt
    except ValueError:
        return "Invalid format"
