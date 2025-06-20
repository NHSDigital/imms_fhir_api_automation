from utilities.config import *
from utilities.resources import apiResources
import uuid

config = getConfigParser()


def get_search_getURLHeader(context):
    context.url = searchGETURL(context.baseUrl)
    context.headers = searchGETHeaders(context.token)
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']

def get_search_postURLHeader(context):
    context.url = searchPOSTURL(context.baseUrl)
    context.headers = searchPOSTHeaders(context.token)
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']

def searchGETURL(url: str ) -> str:
    return url + apiResources.searchGETEndpoint
    

def searchPOSTURL(url: str ) -> str:
    return url + apiResources.searchPOSTEndpoint

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
        "X-Correlation-ID": corID,
        "X-Request-ID": reqID,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/fhir+json",
        "Authorization": "Bearer " + token
        }
    return searchHeaders

