from utilities.config import *
from utilities.helper import *
from utilities.resources import apiResources
import uuid
import json
import os

import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

config = getConfigParser()

def createURL():
    url = config['API']['baseUrl'] + apiResources.createEndpoint
    return url

def createPOSTHeaders(token):
    corID = str(uuid.uuid4())
    reqID = str(uuid.uuid4())
    createHeaders = {
        'X-Correlation-ID': corID,
        'X-Request-ID': reqID,
        'Accept': 'application/fhir+json',
        'Content-Type': 'application/fhir+json',
        'Authorization': 'Bearer ' + token
        }
    return createHeaders

def createPayloadToDelete(NHSNumber,search_keyword):
    NHSNo = str(NHSNumber)
    # guid = str(uuid.uuid4())

    NHSNoPath = "contained.1.identifier.0.value"
    # guidPath = "identifier.0.value"
    # json_requests = updateJSONFiles(search_keyword, f"{NHSNoPath},{guidPath}",f"{NHSNo},{guid}")
    json_requests = updateJSONFiles(search_keyword, f"{NHSNoPath}",f"{NHSNo}")
    json_FileNames, totalFiles = readJSONFileNames(search_keyword)

    return json_requests, json_FileNames, totalFiles


def createPayload(keysToUpdate,valuesToUpdate,search_keyword):

    NHSNumberPath = "contained.1.identifier.0.value"
    birthDatePath = "contained.1.birthDate"
    occurrenceDateTimePath = "occurrenceDateTime"
    recordedPath = "recorded"
    expirationDatePath = "expirationDate"

    updateKeys = str(keysToUpdate).split(",")
    updateValues = str(valuesToUpdate).split(",")
    finalPath = ""
    finalValue = ""

    for updateKey, updateValue in zip(updateKeys, updateValues):
        if updateKey == "NHSNumber":
            NHSNo = str(updateValue)
            finalPath = finalPath + NHSNumberPath + ","
            finalValue = finalValue + NHSNo + ","
        elif updateKey == "birthDate":
            birthDate = str(updateValue)
            finalPath = finalPath + birthDatePath + ","
            finalValue = finalValue + birthDate + ","            
        elif updateKey == "occurrenceDateTime":
            occurrenceDateTime = str(updateValue)
            finalPath = finalPath + occurrenceDateTimePath + ","
            finalValue = finalValue + occurrenceDateTime + ","            
        elif updateKey == "recorded":  
            recorded = str(updateValue)
            finalPath = finalPath + recordedPath + ","
            finalValue = finalValue + recorded + ","            
        elif updateKey == "expirationDate":
            expirationDate = str(updateValue)
            finalPath = finalPath + expirationDatePath + ","
            finalValue = finalValue + expirationDate + ","            

    # guidPath = "identifier.0.value"
    # json_requests = updateJSONFiles(search_keyword, f"{NHSNoPath},{guidPath}",f"{NHSNo},{guid}")
    json_requests = updateJSONFiles(search_keyword, finalPath,finalValue)
    json_FileNames, totalFiles = readJSONFileNames(search_keyword)

    return json_requests, json_FileNames, totalFiles
