from utilities.config import *
from utilities.resources import apiResources
import uuid

config = getConfigParser()

def searchGETURL():
    url = config['API']['baseUrl'] + apiResources.searchGETEndpoint
    return url

def searchPOSTURL():
    url = config['API']['baseUrl'] + apiResources.searchPOSTEndpoint
    return url


def searchContextParam(parameters):
    for row in parameters.table:
        NHSNumber = row['NHSNumber']
        DiseaseType = row['DiseaseType']
        Include = row['Include']
        DateFrom = row['DateFrom']
        DateTo = row['DateTo']

    if (DateFrom == "None" or DateFrom == "") and (DateTo == "None" or DateTo == ""):
        searchParams={'patient.identifier': config['API']['FHIRNHSNumber'] + NHSNumber, '-immunization.target' : DiseaseType, '_include' : Include}
    else:
        searchParams={'patient.identifier': config['API']['FHIRNHSNumber'] + NHSNumber, '-immunization.target' : DiseaseType, '_include' : Include, '-date.from' : DateFrom, '-date.to' : DateTo}

    return searchParams

def searchPaylodParam(patID,immTgt,incl,dtF,dtT):

    searchParams = {}

    if patID.lower() not in ["none", "null", ""]:
        searchParams["patient.identifier"] = config['API']['FHIRNHSNumber'] + patID
    if immTgt.lower() not in ["none", "null", ""]:
        searchParams["-immunization.target"] = immTgt
    if incl.lower() not in ["none", "null", ""]:
        searchParams["_include"] = incl
    if dtF.lower() not in ["none", "null", ""]:
        searchParams["-date.from"] = dtF
    if dtT.lower() not in ["none", "null", ""]:
        searchParams["-date.to"] = dtT
    
    return searchParams


def searchPaylodPatIdParam(patID,NhsNo,immTgt,incl,dtF,dtT):

    searchParams = {}

    if patID.lower() not in ["none", "null", ""] and NhsNo.lower() not in ["none", "null", ""]:
        searchParams["patient.identifier"] = patID + "|" + NhsNo
    if immTgt.lower() not in ["none", "null", ""]:
        searchParams["-immunization.target"] = immTgt
    if incl.lower() not in ["none", "null", ""]:
        searchParams["_include"] = incl
    if dtF.lower() not in ["none", "null", ""]:
        searchParams["-date.from"] = dtF
    if dtT.lower() not in ["none", "null", ""]:
        searchParams["-date.to"] = dtT
    
    return searchParams


def searchGETHeaders(token):
    corID = str(uuid.uuid4())
    reqID = str(uuid.uuid4())
    searchHeaders = {
        'X-Correlation-ID': corID,
        'X-Request-ID': reqID,
        'Accept': 'application/fhir+json',
        'Authorization': 'Bearer ' + token
        }
    return searchHeaders


def searchPOSTHeaders(token):
    corID = str(uuid.uuid4())
    reqID = str(uuid.uuid4())
    searchHeaders = {
        'X-Correlation-ID': corID,
        'X-Request-ID': reqID,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/fhir+json',
        'Authorization': 'Bearer ' + token
        }
    return searchHeaders

