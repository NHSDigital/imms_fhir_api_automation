import glob
import itertools
from urllib.parse import urlencode
import requests
import json
import re
import boto3
import requests
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.SearchPostObject import *
from utilities.payloadSearch import *
from utilities.payloadCreate import *
from utilities.config import *
from utilities.dynamodbHelper import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
import logging
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from features.steps.common_steps import *
from datetime import datetime



config = getConfigParser()


logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)


scenarios("search.feature")

@given("I have created a valid vaccination record")
def validVaccinationRecordIsCreated(context):
    valid_json_payload_is_created(context)
    Trigger_the_post_create_request(context)
    The_request_will_be_successful_with_the_status_code(context, 201)
    validateCreateLocation(context)

@when("Send a search request with POST method for Immunization event create")
def TiggerSearchPostRequest(context):
    context.url = searchPOSTURL(context.baseUrl)
    context.headers = searchPOSTHeaders(context.token)
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']
    context.request = convert_to_form_data(set_request_data(context.patient.identifier[0].value, context.vaccine_type, datetime.today().strftime("%Y-%m-%d")))
    #context.request = "patient.identifier=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number|9449309981&-immunization.target=COVID19&_include=Immunization:patient&-date.from=2025-05-01"
    print(f"Type of form_data: {type(context.request)}")
    print(f"Search Post request {context.request}")
    print(f"headers are {context.headers}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)
    print(f"Search Post response {context.response.json()}")

# @given('After passing all the valid parameters')
# def queryParamSearch(context):  
#     context.getUrl = searchGETURL()
#     context.params = searchContextParam(context)
#     context.headersGet = searchGETHeaders(context.token)

# @when('Send a search request with GET method')
# def GETAPISearch(context):
#     context.response = requests.get(context.getUrl, params = context.params, headers = context.headersGet)

# @when('Send a search request with POST method')
# def GETAPISearch(context):
#     context.response = requests.post(context.postUrl, data = context.params, headers = context.headersPost)    


# @then('The search will be successful with the status code 200')
# def APIResponseStatus(context):
#     statusCode = context.response.status_code
#     resText = context.response.text
#     assert statusCode == 200, f"Failed to get the status code 200. Status code Received: {statusCode}. Response: {resText}"
#     # context.soft_assertions.assert_condition(statusCode == 200, f"Status Code of the Response API: {statusCode}")


# @given('After passing all the valid parameters except an invalid nhsnumber')
# def invalidNHSNoSearch(context):
#     context.getUrl = searchGETURL()
#     context.params = searchContextParam(context)
#     context.headersGet = searchGETHeaders(context.token)

# @then('The search will throw error with the status code 400')
# def errorCode4xx(context):
#     context.statusCode = context.response.status_code
#     context.resText = context.response.text
#     assert context.statusCode == 400, f"Failed to get the status code 400. Status code Received: {context.statusCode}. Response: {context.resText}"
#     # context.soft_assertions.assert_condition(result['MAKE'] == MAKE, f"Make match: {result['MAKE']} = {MAKE}")

# @then('The Search Response JSONs should contain the error message for invalid NHS Number') 
# def operationOutcomeInvalidNHSNo(context):
#     # code = config['OPERATIONOUTCOME']['codeInvalid']
#     # diagnostics = config['OPERATIONOUTCOME']['diagnosticsInvalid']
#     code = config['OPERATIONOUTCOME']['codeInvariant']
#     diagnostics = config['OPERATIONOUTCOME']['diagnosticsInvariant']    
#     resourceType = config['OPERATIONOUTCOME']['resourceType']

#     resActual = json.loads(context.resText)
#     resExpected = json.loads(operationOutcomeResJson(code, diagnostics))

#     idPattern = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

#     with allure.step(f"Validating Operation Outcome fields for the NHS Number: {context.NHSNumber}"):
#         validate_json_fields(resourceType, resActual['resourceType'], path="resourceType")
#         validate_json_fields(idPattern, resActual['id'], path="id")
#         validate_json_fields(resExpected['meta'], resActual['meta'], path="meta")
#         validate_json_fields(resExpected['issue'], resActual['issue'], path="issue")

#         soft_assertions.assert_all()

# @then('The Search Response JSONs should contain the valid error message for mandatory query parameters') 
# def operationOutcomeNullParam(context):
#     if context.NHSNumber.lower() in ["none", "null", ""]:
#         code = config['OPERATIONOUTCOME']['codeInvalid']
#         diagnostics = config['OPERATIONOUTCOME']['diagnosticsNHSNoInvalid']
#     if context.DiseaseType.lower() in ["none", "null", ""]:
#         code = config['OPERATIONOUTCOME']['codeInvalid']
#         diagnostics = config['OPERATIONOUTCOME']['diagnosticsDiseaseTypeInvalid']
#     resourceType = config['OPERATIONOUTCOME']['resourceType']

#     resActual = json.loads(context.resText)
#     resExpected = json.loads(operationOutcomeResJson(code, diagnostics))

#     idPattern = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

#     with allure.step(f"Validating Operation Outcome fields for the NHS Number: {context.NHSNumber}"):
#         validate_json_fields(resourceType, resActual['resourceType'], path="resourceType")
#         validate_json_fields(idPattern, resActual['id'], path="id")
#         validate_json_fields(resExpected['meta'], resActual['meta'], path="meta")
#         validate_json_fields(resExpected['issue'], resActual['issue'], path="issue")

#         soft_assertions.assert_all()        


# @then('The Search Response JSONs should contain the valid error message for invalid format of patient identifier') 
# def operationOutcomeInvalidPatIdParam(context):
#     code = config['OPERATIONOUTCOME']['codeInvalid']
#     diagnostics = config['OPERATIONOUTCOME']['diagnosticsFormatInvalid']

#     resourceType = config['OPERATIONOUTCOME']['resourceType']

#     resActual = json.loads(context.resText)
#     resExpected = json.loads(operationOutcomeResJson(code, diagnostics))

#     idPattern = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

#     with allure.step(f"Validating Operation Outcome fields for the Patient Identifier: {context.PatientIdentifier}"):
#         validate_json_fields(resourceType, resActual['resourceType'], path="resourceType")
#         validate_json_fields(idPattern, resActual['id'], path="id")
#         validate_json_fields(resExpected['meta'], resActual['meta'], path="meta")
#         validate_json_fields(resExpected['issue'], resActual['issue'], path="issue")

#         soft_assertions.assert_all()   



# @given('With invalid format of the patient identifier "{PatientIdentifier}" and valid "{NHSNumber}", "{DiseaseType}", "{Include}", "{DateFrom}" & "{DateTo}" parameters')
# def invalidPatIdSearch(context,PatientIdentifier,NHSNumber,DiseaseType,Include,DateFrom,DateTo):    
#     context.getUrl = searchGETURL()
#     context.postUrl = searchPOSTURL()
#     context.params = searchPaylodPatIdParam(PatientIdentifier,NHSNumber,DiseaseType,Include,DateFrom,DateTo)
#     context.headersGet = searchGETHeaders(context.token)  
#     context.headersPost = searchPOSTHeaders(context.token)  
#     context.PatientIdentifier = PatientIdentifier + NHSNumber 

# @given('With any of the mandatory parameters "{NHSNumber}" or "{DiseaseType}" are null and "{Include}", "{DateFrom}" & "{DateTo}" parameters havning valid value')
# def nullNHSNoParamSearch(context,NHSNumber,DiseaseType,Include,DateFrom,DateTo):
#     context.getUrl = searchGETURL()
#     context.postUrl = searchPOSTURL()
#     context.params = searchPaylodParam(NHSNumber,DiseaseType,Include,DateFrom,DateTo)
#     context.headersGet = searchGETHeaders(context.token)  
#     context.headersPost = searchPOSTHeaders(context.token)  
#     context.NHSNumber = NHSNumber 
#     context.DiseaseType = DiseaseType 

# @given(u'With the invalid "{NHSNumber}" and valid "{DiseaseType}", "{Include}", "{DateFrom}" & "{DateTo}" parameters')
# def invalidNHSNoParamSearch(context,NHSNumber,DiseaseType,Include,DateFrom,DateTo):
#     context.getUrl = searchGETURL()
#     context.postUrl = searchPOSTURL()
#     context.params = searchPaylodParam(NHSNumber,DiseaseType,Include,DateFrom,DateTo)
#     context.headersGet = searchGETHeaders(context.token)  
#     context.headersPost = searchPOSTHeaders(context.token)  
#     context.NHSNumber = NHSNumber 

  
# @given('With the valid "{NHSNumber}", "{DiseaseType}", "{Include}", "{DateFrom}" & "{DateTo}" parameters')
# def validParamSearch(context,NHSNumber,DiseaseType,Include,DateFrom,DateTo):
#     context.getUrl = searchGETURL()
#     context.postUrl = searchPOSTURL()
#     context.params = searchPaylodParam(NHSNumber,DiseaseType,Include,DateFrom,DateTo)
#     context.headersGet = searchGETHeaders(context.token) 
#     context.headersPost = searchPOSTHeaders(context.token)   
#     context.NHSNumber = NHSNumber

# @given('Create an immunization event for the patient with the input JSONs available')
# def cretaeImms(context):
#         context.createUrl = createURL()
#         # context.createPayload = createPayload(context.NHSNumber,"search")
#         context.createPayload = createPayload("NHSNumber",context.NHSNumber,"create")
#         context.createHeaders = createPOSTHeaders(context.token)
#         context.responseImmsID = {}
#         context.requestJSON = context.createPayload[0]
#         context.requestFileName = context.createPayload[1]
#         context.requestTotalFiles = context.createPayload[2]
        
#         for fileName in context.requestFileName:
#             response = requests.post(context.createUrl, json=context.requestJSON[fileName], headers=context.createHeaders)
#             assert response.status_code == 201, f"Failed to create immunization event for {fileName}. Status code: {response.status_code}. Response: {response.text}"
#             context.responseImmsID[fileName] = response.headers['Location'].split("/")[-1]

# @when('Send a search request with GET method for each Immunization event created')
# def searchGETAPI(context):
#     context.responseJsons = {}
#     context.responseStatus = {}

#     for fileName in context.requestFileName:
#         responseSearch = requests.get(context.getUrl, params = context.params, headers = context.headersGet)
#         context.responseJsons[fileName] = responseSearch.text
#         context.responseStatus[fileName] = responseSearch.status_code


# @when('Send a search request with POST method for each Immunization event created')
# def searchPOSTAPI(context):
#     context.responseJsons = {}
#     context.responseStatus = {}

#     for fileName in context.requestFileName:      
#         responseSearch = requests.post(context.postUrl, data = context.params, headers = context.headersPost)
#         context.responseJsons[fileName] = responseSearch.text
#         context.responseStatus[fileName] = responseSearch.status_code        


# @then('The search will be successful with the status code 200 for each Immunization event')
# def validateSearchAPIStatusCode(context):
#     for fileName in context.requestFileName:
#         statusCode = context.responseStatus[fileName]
#         response = context.responseJsons[fileName]
#         assert statusCode == 200, f"Failed to search for immunization event for {fileName}. Status code: {statusCode}. Response:{response}"        


@then('The Search Response JSONs should contain the detail of the immunization events created above')
def validateImmsID(context):
    context.finalResponseJson = {}
    context.finalResponseJsonPat = {}
    context.expectedImmsID = {}
    for fileName in context.requestFileName:
        context.expectedImmsID[fileName] = context.responseImmsID[fileName]

        responseJsonLoad = json.loads(context.responseJsons[fileName])
        
        idFound = False
        findEntry = 0
        for entry in responseJsonLoad['entry']:
            if entry['resource']['id'] == context.expectedImmsID[fileName]:
                context.finalResponseJson[fileName] = responseJsonLoad['entry'][findEntry]
                idFound = True
                break
            findEntry = findEntry + 1
        assert idFound, f"Immunization ID {context.expectedImmsID[fileName]} not found in search response for {fileName}"
        
        for entry in responseJsonLoad['entry']:
            context.finalResponseJsonPat[fileName] = responseJsonLoad['entry'][-1]
        assert len(context.finalResponseJsonPat) > 0, f"Patient entry {context.NHSNumber} not found in search response for {fileName}"


@then('The Search Response JSONs field values should match with the input JSONs field values for resourceType Immunization')
def validateJsonImms(context):

    for fileName in context.requestFileName:
        reqJson = context.requestJSON[fileName] 
        resJson = context.finalResponseJson[fileName]

        fullUrlRes = config['SEARCH']['fullUrlRes'] + context.expectedImmsID[fileName]
        performerReq = reqJson["performer"][int(config['SEARCH']['performerFieldNoReq'])]
        performerRes = resJson["resource"]["performer"][int(config['SEARCH']['performerFieldNoRes'])]
        contPatientFieldNoIdReq = reqJson["contained"][int(config['SEARCH']['containedPatientFieldNoReq'])]['identifier'][int(config['SEARCH']['patientIdFieldNoReq'])]
        contPatientFieldNoIdRes = resJson["resource"]["patient"]["identifier"]
        referencePattern = r"^urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"       

        with allure.step(f"Validating JSON fields for {fileName} and the immunization event {context.expectedImmsID[fileName]}"):
            validate_json_fields(fullUrlRes, resJson['fullUrl'], path="fullUrl")
            validate_json_fields(reqJson['resourceType'], resJson['resource']['resourceType'], path="resourceType")
            validate_json_fields(reqJson['extension'], resJson['resource']['extension'], path="extension") 
            validate_json_fields(reqJson['identifier'], resJson['resource']['identifier'], path="identifier")  
            validate_json_fields(reqJson['status'], resJson['resource']['status'], path="status") 
            validate_json_fields(reqJson['vaccineCode'], resJson['resource']['vaccineCode'], path="vaccineCode") 
            validate_json_fields(format_timestamp(reqJson['occurrenceDateTime']), format_timestamp(resJson['resource']['occurrenceDateTime']), path="occurrenceDateTime")
            validate_json_fields(format_timestamp(reqJson['recorded']), format_timestamp(resJson['resource']['recorded']), path="recorded")
            validate_json_fields(reqJson['primarySource'], resJson['resource']['primarySource'], path="primarySource")
            validate_json_fields(reqJson['manufacturer'], resJson['resource']['manufacturer'], path="manufacturer")
            validate_json_fields(reqJson['location'], resJson['resource']['location'], path="location")
            validate_json_fields(reqJson['lotNumber'], resJson['resource']['lotNumber'], path="lotNumber")
            validate_json_fields(reqJson['expirationDate'], resJson['resource']['expirationDate'], path="expirationDate")
            validate_json_fields(reqJson['site'], resJson['resource']['site'], path="site")
            validate_json_fields(reqJson['route'], resJson['resource']['route'], path="route")
            validate_json_fields(reqJson['doseQuantity'], resJson['resource']['doseQuantity'], path="doseQuantity")
            validate_json_fields(performerReq, performerRes, path="performer")                       
            validate_json_fields(reqJson['reasonCode'], resJson['resource']['reasonCode'], path="reasonCode")
            validate_json_fields(reqJson['protocolApplied'], resJson['resource']['protocolApplied'], path="protocolApplied")
            validate_json_fields(contPatientFieldNoIdReq, contPatientFieldNoIdRes, path="patient.identifier")
            validate_json_fields("Patient", resJson['resource']['patient']['type'], path="patient.type")
            # validate_json_fields(referencePattern, resJson['resource']['patient']['reference'], path="patient.reference")
            soft_assertions.assert_condition(bool(re.match(referencePattern, resJson['resource']['patient']['reference'])), f"patient.reference. Expected guid pattern, Found {resJson['resource']['patient']['reference']}")
            validate_json_fields("match", resJson['search']['mode'], path="search.mode")

            soft_assertions.assert_all()

@then('The Search Response JSONs field values should match with the input JSONs field values for resourceType Patient')
def validateJsonPat(context):
    for fileName in context.requestFileName:
        reqJson = context.requestJSON[fileName] 
        resJson = context.finalResponseJsonPat[fileName]

        fullUrlPattern = r"^urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"  
        contPatientFieldNoIdReq = reqJson["contained"][int(config['SEARCH']['containedPatientFieldNoReq'])]['identifier']
        contPatientFieldNoIdRes = resJson["resource"]["identifier"]

        with allure.step(f"Validating JSON fields for {fileName} and the patient {context.NHSNumber}"):
            soft_assertions.assert_condition(bool(re.match(fullUrlPattern, resJson['fullUrl'])), f"patient.fullUrl. Expected guid pattern, Found {resJson['fullUrl']}")
            # validate_json_fields(fullUrlPattern, resJson['fullUrl'], path="fullUrl")
            validate_json_fields("Patient", resJson['resource']['resourceType'], path="resourceType")
            validate_json_fields(context.NHSNumber, resJson['resource']['id'], path="id")
            validate_json_fields(contPatientFieldNoIdReq, contPatientFieldNoIdRes, path="identifier")
            validate_json_fields("include", resJson['search']['mode'], path="search.mode")

            soft_assertions.assert_all()
