import requests
from pytest_bdd import given, when, then, parsers
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.immunization_builder import *
from utilities.payloadSearch import *
from utilities.payloadCreate import *
from utilities.config import *
import pytest_check as check

@given("Valid json payload is created")
def valid_json_payload_is_created(context):
    context.patient = load_patient_by_id(context.patient_id)
    context.immunization_object = create_immunization_object(context.patient, context.vaccine_type)
    
@when("Trigger the post create request")
def Trigger_the_post_create_request(context):
    context.url = createURL(context.baseUrl)
    context.headers = createPOSTHeaders(context.token)
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']
    context.create_object = context.immunization_object
    context.request = context.create_object.dict(exclude_none=True, exclude_unset=True)

    # context.create_object = clean_dataclass(context.immunization_object)
    # context.request = deep_asdict(context.create_object)
    context.response = requests.post(context.url, json=context.request, headers=context.headers)
    print(f"Create Request is {json.dumps(context.request)}" )
    print(f"Create Request is {context.response}" )

@then(parsers.parse("The request will be unsuccessful with the status code '{statusCode}'"))
@then(parsers.parse("The request will be successful with the status code '{statusCode}'"))
def The_request_will_be_successful_with_the_status_code(context, statusCode):
    assert context.response.status_code == int(statusCode)


@then('The location key in header will contain the Immunization Id')
def validateCreateLocation(context):
    location = context.response.headers['location']
    assert  "location" in context.response.headers, f"Location header is missing in the response with Status code: {context.response.statusCode}. Response: {context.response.json()}"
    context.location = location.split("/")[-1]
    print(f"Location is {context.location}")
    check.is_true(
        context.location is not None, 
        f"Expected IdentifierPK: {context.patient.identifier[0].value}, Found: {context.location}"
    )