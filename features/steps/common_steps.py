import json
from venv import logger
import requests
from pytest_bdd import given, when, then, parsers
from src.dynamoDB.dynamoDBHelper import *
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.immunization_builder import *
from utilities.FHIRImmunizationHelper import *
from utilities.enums import Operation
from utilities.getHeader import *
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
    
@given("I have created a valid vaccination record")
def validVaccinationRecordIsCreated(context):
    valid_json_payload_is_created(context)
    Trigger_the_post_create_request(context)
    The_request_will_have_status_code(context, 201)
    validateCreateLocation(context)
    
@when("Trigger the post create request")
def Trigger_the_post_create_request(context):
    get_create_postURLHeader(context)
    context.create_object = context.immunization_object
    context.request = context.create_object.dict(exclude_none=True, exclude_unset=True)
    context.response = requests.post(context.url, json=context.request, headers=context.headers)
    print(f"Create Request is {json.dumps(context.request)}" )

@then(parsers.parse("The request will be unsuccessful with the status code '{statusCode}'"))
@then(parsers.parse("The request will be successful with the status code '{statusCode}'"))
def The_request_will_have_status_code(context, statusCode):
    print(context.response.status_code)
    print(int(statusCode))
    assert context.response.status_code == int(statusCode), f"\n Expected status code: {statusCode}, but got: {context.response.status_code}. Response: {context.response.json()} \n"


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
        (not is_valid_date(context.DateFrom), "invalid_DateFrom") if getattr(context, "DateFrom", None) else (False, None),
        (not is_valid_date(context.DateTo), "invalid_DateTo") if getattr(context, "DateTo", None) else (False, None),
        (not is_valid_nhs_number(context.NHSNumber), "invalid_NHSNumber"),
    ]

    for failed, errorName in error_checks:
        if failed:
            break
    else:
        raise ValueError("All parameters are valid, no error expected.")

    if errorName:
        validateErrorResponse(error_response, errorName)
        print(f"\n Error Response - \n {error_response}")    
        
@then('The X-Request-ID and X-Correlation-ID keys in header will populate correctly')
def validateCreateHeader(context):
    assert "X-Request-ID" in context.response.request.headers, "X-Request-ID missing in headers"
    assert "X-Correlation-ID" in context.response.request.headers, "X-Correlation-ID missing in headers"
    assert context.response.request.headers["X-Request-ID"] == context.reqID, "X-Request-ID incorrect"
    assert context.response.request.headers["X-Correlation-ID"] == context.corrID, "X-Correlation-ID incorrect"   
    
@then(parsers.parse("The imms event table will be populated with the correct data for '{operation}' event"))
def validate_imms_event_table_by_operation(context, operation: Operation):
    create_obj = context.create_object
    table_query_response = fetch_immunization_events_detail(context.aws_profile_name, context.ImmsID)
    assert "Item" in table_query_response, f"Item not found in response for ImmsID: {context.ImmsID}"
    item = table_query_response["Item"]

    resource_json_str = item.get("Resource")
    assert resource_json_str, "Resource field missing in item."

    try:
        resource = json.loads(resource_json_str)
    except (TypeError, json.JSONDecodeError) as e:
        logger.error(f"Failed to parse Resource from item: {e}")
        raise AssertionError("Failed to parse Resource from response item.")

    assert resource is not None, "Resource is None in the response"
    created_event = parse_imms_int_imms_event_response(resource)

    fields_to_compare = [
        ("Operation", Operation[operation].value, item.get("Operation")),
        ("SupplierSystem", "Postman_Auth", item.get("SupplierSystem")),
        ("PatientPK", f"Patient#{context.patient.identifier[0].value}", item.get("PatientPK")),
        ("PatientSK", f"{context.vaccine_type}#{context.ImmsID}", item.get("PatientSK")),
        ("Version", 1, item.get("Version")),
    ]
    
    for name, expected, actual in fields_to_compare:
        check.is_true(
                expected == actual,
                f"Expected {name}: {expected}, Actual {actual}"
            )
        
    validateToCompareRequestAndResponse(context, create_obj, created_event, True)
      