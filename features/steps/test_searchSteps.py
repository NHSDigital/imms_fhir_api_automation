from urllib.parse import urlencode
import requests
import requests
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.SearchObject import *
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
    The_request_will_have_status_code(context, 201)
    validateCreateLocation(context)

@given(parsers.parse("Valid vaccination record is created with Patient '{Patient}' and vaccine_type '{vaccine_type}'"))
def validVaccinationRecordIsCreatedWithPatient(context, Patient, vaccine_type):
    The_Immunization_object_is_created_with_patient_for_vaccine_type(context, Patient, vaccine_type)
    Trigger_the_post_create_request(context)
    The_request_will_have_status_code(context, 201)
    validateCreateLocation(context)

@when("Send a search request with GET method for Immunization event created")
def TiggerSearchGetRequest(context):
    get_search_getURLHeader(context)
    context.params = convert_to_form_data(set_request_data(context.patient.identifier[0].value, context.vaccine_type, datetime.today().strftime("%Y-%m-%d")))
    print(f"\n Search Get Parameters - \n {context.params}")
    context.response = requests.get(context.url, params = context.params, headers = context.headers)
    
    print(f"\n Search Get Response - \n {context.response.json()}")

@when("Send a search request with POST method for Immunization event created")
def TiggerSearchPostRequest(context):
    get_search_postURLHeader(context)
    context.request = convert_to_form_data(set_request_data(context.patient.identifier[0].value, context.vaccine_type, datetime.today().strftime("%Y-%m-%d")))
    print(f"\n Search Post Request - \n {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)
    
    print(f"\n Search Post Response - \n {context.response.json()}")    
    
@when(parsers.parse("Send a search request with POST method for invalid NHS Number '{NHSNumber}'"))
def send_search_post_request(context, NHSNumber):
    get_search_postURLHeader(context)
    if NHSNumber.lower() in ["none", "null", ""]:
        NHSNumber = ""
    context.request = convert_to_form_data(set_request_data(NHSNumber, context.vaccine_type, datetime.today().strftime("%Y-%m-%d")))
    print(f"\n Search Post request {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)


@when(parsers.parse("Send a search request with POST method With the '{NHSNumber}' and invalid '{DiseaseType}'"))
def send_invalid_disease_type_post_request(context, NHSNumber, DiseaseType):
    get_search_postURLHeader(context)
    context.request = convert_to_form_data(set_request_data(NHSNumber, DiseaseType, datetime.today().strftime("%Y-%m-%d")))
    print(f"\n Search Post request {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)


@then('The Search Response JSONs should contain the error message for invalid NHS Number')    
def operationOutcomeInvalidNHSNo(context):
    error_response = parse_errorResponse(context.response.json())
    errorName= "invalid_NHSNumber"
    validateErrorResponse(error_response, errorName)
    print(f"\n Error Response - \n {error_response}")
    
@then('The Search Response JSONs should contain the error message for invalid Disease Type')    
def operationOutcomeInvalidNHSNo(context):
    error_response = parse_errorResponse(context.response.json())
    errorName= "invalid_DiseaseType"
    validateErrorResponse(error_response, errorName)
    print(f"\n Error Response - \n {error_response}")

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

@then('The Search Response JSONs should contain the detail of the immunization events created above')
def validateImmsID(context):
    data = context.response.json()
    context.parsed_search_object = parse_FHIRImmunizationResponse(data)

    context.created_event = find_entry_by_Imms_id(context.parsed_search_object, context.ImmsID)

    # print(f"{data}\n")
    # print(f"{context.parsed_search_object}\n")
    # print(f"{context.created_event}\n")
    
    if context.created_event is None:
        raise AssertionError(f"No object found with Immunisation ID {context.ImmsID} in the search response.")
    
    patient_reference = getattr(context.created_event.resource.patient, "reference", None)

    if not patient_reference:
        raise ValueError("Patient reference is missing in the found event.")

    # Assign to context for further usage
    context.Patient_fullUrl = patient_reference


@then('The Search Response JSONs field values should match with the input JSONs field values for resourceType Immunization')
def validateJsonImms(context):
    create_obj = context.create_object
    created_event= context.created_event.resource
    validateToCompareRequestAndResponse(context, create_obj, created_event)


@then('The Search Response JSONs field values should match with the input JSONs field values for resourceType Patient')
def validateJsonPat(context):        
    response_patient_entry =  find_patient_by_fullurl(context.parsed_search_object)
    assert response_patient_entry is not None, f"No Patient found with fullUrl {context.Patient_fullUrl}"
    
    response_patient = response_patient_entry.resource
    expected_nhs_number = context.create_object.contained[1].identifier[0].value
    actual_nhs_number = response_patient.identifier[0].value
    expected_system = context.create_object.contained[1].identifier[0].system    
    actual_system = response_patient.identifier[0].system

    fields_to_compare = [
        ("fullUrl", context.Patient_fullUrl, response_patient_entry.fullUrl),

        ("resourceType", "Patient", response_patient.resourceType),
        ("id", expected_nhs_number, response_patient.id),
        ("identifier.system", expected_system, actual_system),
        ("identifier.value", expected_nhs_number, actual_nhs_number),
    ]

    for name, expected, actual in fields_to_compare:
            check.is_true(
                expected == actual,
                f"Expected {name}: {expected}, Actual {actual}"
            )
