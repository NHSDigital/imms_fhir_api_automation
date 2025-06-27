from utilities.config import *
from utilities.FHIRImmunizationHelper import *
from utilities.resources import apiResources
import uuid
import json
import os

import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_create_postURLHeader(context):
    context.url = createURL(context.baseUrl)
    context.headers = createPOSTHeaders(context.token)
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']

def createURL(url: str ):
    url = url + apiResources.createEndpoint
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

