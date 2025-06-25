import requests
from pytest_bdd import given, when, then, parsers
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.immunization_builder import *
from utilities.FHIRImmunizationHelper import *
from utilities.payloadSearch import *
from utilities.payloadCreate import *
from utilities.config import *
import pytest_check as check

@given("Valid json payload is created")
def valid_json_payload_is_created(context):
    context.patient = load_patient_by_id(context.patient_id)
    context.immunization_object = create_immunization_object(context.patient, context.vaccine_type)

@given(parsers.parse("Valid json payload is created with Patient '{Patient}' and vaccine_type '{vaccine_type}'"))
def The_Immunization_object_is_created_with_patient_for_vaccine_type(context, Patient, vaccine_type):
    context.vaccine_type = vaccine_type
    context.patient_id = Patient
    context.patient = load_patient_by_id(context.patient_id)
    context.immunization_object = create_immunization_object(context.patient, context.vaccine_type)

@when("Trigger the post create request")
def Trigger_the_post_create_request(context):
    get_create_postURLHeader(context)
    context.create_object = context.immunization_object
    context.request = context.create_object.dict(exclude_none=True, exclude_unset=True)
    context.response = requests.post(context.url, json=context.request, headers=context.headers)
    print(f"Create Request is {json.dumps(context.request)}" )
    # print(f"Create Response is {context.response}" )

@then(parsers.parse("The request will be unsuccessful with the status code '{statusCode}'"))
@then(parsers.parse("The request will be successful with the status code '{statusCode}'"))
def The_request_will_have_status_code(context, statusCode):
    assert context.response.status_code == int(statusCode)


@then('The location key in header will contain the Immunization Id')
def validateCreateLocation(context):
    location = context.response.headers['location']
    assert  "location" in context.response.headers, f"Location header is missing in the response with Status code: {context.response.statusCode}. Response: {context.response.json()}"
    context.ImmsID = location.split("/")[-1]
    print(f"\n Immunisation ID is {context.ImmsID}")
    check.is_true(
        context.ImmsID is not None, 
        f"Expected IdentifierPK: {context.patient.identifier[0].value}, Found: {context.ImmsID}"
    )

@then('The Search Response JSONs should contain correct error message for invalid NHS Number')   
@then('The Search Response JSONs should contain correct error message for invalid Disease Type')   
@then('The Search Response JSONs should contain correct error message for invalid Date From')
@then('The Search Response JSONs should contain correct error message for invalid Date To') 
def operationOutcomeInvalidParams(context):
    error_response = parse_errorResponse(context.response.json())
    
    error_checks = [
        (not is_valid_disease_type(context.DiseaseType), "invalid_DiseaseType"),
        (not is_valid_date(context.DateFrom), "invalid_DateFrom"),
        (not is_valid_date(context.DateTo), "invalid_DateTo"),
        (not is_valid_nhs_number(context.NHSNumber), "invalid_NHSNumber"),
    ]

    for failed, errorName in error_checks:
        if failed:
            break
    else:
        raise ValueError("Both parameters are valid, no error expected.")
    
    validateErrorResponse(error_response, errorName)
    print(f"\n Error Response - \n {error_response}")    