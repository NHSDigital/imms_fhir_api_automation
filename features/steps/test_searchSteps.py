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
from utilities.FHIRImmunizationHelper import *
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
    print(f"Search Post request {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)
    
@when(parsers.parse("Send a search request with POST method With the invalid '{NHSNumber}'"))
def send_invalid_post_request(context, NHSNumber):
    context.url = searchPOSTURL(context.baseUrl)
    context.headers = searchPOSTHeaders(context.token)
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']
    context.request = convert_to_form_data(set_request_data(NHSNumber, context.vaccine_type, datetime.today().strftime("%Y-%m-%d")))
    print(f"Search Post request {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)

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

@then('The Search Response JSONs should contain the error message for invalid NHS Number') 
def operationOutcomeInvalidNHSNo(context):
    error_response = parse_errorResponse(context.response.json())

    errorName= "invalid_NHSNumber"
    
    
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
    data = context.response.json()
    context.parsed_search_object = parse_FHIRImmunizationResponse(data)

    context.created_event = find_entry_by_Imms_id(context.parsed_search_object, context.location)
    
    if context.created_event is None:
        raise AssertionError(f"No object found with {context.location}")

    patient_reference = getattr(context.created_event.resource.patient, "reference", None)

    if not patient_reference:
        raise ValueError("Patient reference is missing in the found event.")

    # Assign to context for further usage
    context.Patient_fullUrl = patient_reference

    print(f"Event is found: {context.created_event}")
    # context.finalResponseJson = {}
    # context.finalResponseJsonPat = {}
    # context.expectedImmsID = {}
    # for fileName in context.requestFileName:
    #     context.expectedImmsID[fileName] = context.responseImmsID[fileName]

    #     responseJsonLoad = json.loads(context.responseJsons[fileName])
        
    #     idFound = False
    #     findEntry = 0
    #     for entry in responseJsonLoad['entry']:
    #         if entry['resource']['id'] == context.expectedImmsID[fileName]:
    #             context.finalResponseJson[fileName] = responseJsonLoad['entry'][findEntry]
    #             idFound = True
    #             break
    #         findEntry = findEntry + 1
    #     assert idFound, f"Immunization ID {context.expectedImmsID[fileName]} not found in search response for {fileName}"
        
    #     for entry in responseJsonLoad['entry']:
    #         context.finalResponseJsonPat[fileName] = responseJsonLoad['entry'][-1]
    #     assert len(context.finalResponseJsonPat) > 0, f"Patient entry {context.NHSNumber} not found in search response for {fileName}"

@then('The Search Response JSONs field values should match with the input JSONs field values for resourceType Immunization')
def validateJsonImms(context):
    create_obj = context.create_object
    created_event= context.created_event.resource
    request_patient = create_obj.contained[1]
    response_patient = created_event.patient
    check.is_true (request_patient.identifier[0].value== response_patient.identifier.value,
                    f"expected patient NHS Number {request_patient.identifier[0].value}  actual nhs number {response_patient.identifier.value}")
    referencePattern = r"^urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
     
    check.is_true(re.match(referencePattern, response_patient.reference), 
                  f"Expected reference {referencePattern} Invalid reference format: {referencePattern}")
    
    check.is_true("Patient"== response_patient.type,
                   f"Expected is  Patient nut actual patient Type is : {response_patient.type}")
    
    expected_recorded = covert_to_expected_date_format(context.create_object.recorded)

    expected_fullUrl = config['SEARCH']['fullUrlRes'] + context.location

    fields_to_compare = [
        ("FullUrl", expected_fullUrl, context.created_event.fullUrl),
        ("status", create_obj.status, created_event.status),
        ("Recorded", expected_recorded, created_event.recorded),
        ("lotNumber", create_obj.lotNumber, created_event.lotNumber),
        ("expirationDate", create_obj.expirationDate, created_event.expirationDate),
        ("primarySource", create_obj.primarySource, created_event.primarySource),
        ("doseQuantity", create_obj.doseQuantity, created_event.doseQuantity),
        ("site", create_obj.site, created_event.site),
        ("manufacturer", create_obj.manufacturer, created_event.manufacturer),
        ("vaccineCode", create_obj.vaccineCode, created_event.vaccineCode),
        ("reasonCode", create_obj.reasonCode, created_event.reasonCode),
        ("protocolApplied", create_obj.protocolApplied, created_event.protocolApplied),
    ]

    for name, expected, actual in fields_to_compare:
        check.is_true(
            expected == actual,
            f"Expected {name}: {expected}, got {actual}"
        )

@then('The Search Response JSONs field values should match with the input JSONs field values for resourceType Patient')
def validateJsonPat(context):        
    response_patient_entry =  find_patient_by_fullurl(context.parsed_search_object)
    assert response_patient_entry is not None, f"No Patient found with fullUrl {context.Patient_fullUrl}"
    print(f"Patient entry is :{response_patient_entry}")
    
    response_patient = response_patient_entry.resource
    check.is_true(context.Patient_fullUrl == response_patient_entry.fullUrl, f"Expected Patient ful, got {response_patient_entry.fullUrl}")
    expected_nhs_number = context.create_object.contained[1].identifier[0].value     

    check.is_true(response_patient.resourceType == "Patient", f"Expected Patient resource, got {response_patient.resourceType}")
    check.is_true(response_patient.id == expected_nhs_number, f"Expected Patient ID {expected_nhs_number}, got {response_patient.id}")
    
    actual_nhs_number = response_patient.identifier[0].value
    check.is_true(actual_nhs_number == expected_nhs_number, f"Expected Patient Identifier value {expected_nhs_number}, got {actual_nhs_number}")

    actual_system = response_patient.identifier[0].system
    expected_system = context.create_object.contained[1].identifier[0].system
    check.is_true(actual_system == expected_system, f"Expected Patient Identifier system {expected_system}, got {actual_system}")
