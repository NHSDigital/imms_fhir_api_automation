import boto3
import requests
from src.dynamoDB.dynamoDBHelper import *
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from utilities.FHIRImmunizationHelper import *
from utilities.payloadSearch import *
from utilities.payloadCreate import *
from utilities.config import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
import logging
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from features.steps.common_steps import *

config = getConfigParser()


logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)


scenarios("create.feature")

@given('Valid json payload is created where vaccination procedure term has text filed populated')
def createValidJsonPayloadWithProcedureText(context):
    valid_json_payload_is_created(context)
    context.immunization_object.extension = [
        build_vaccine_procedure_extension(context.vaccine_type.upper(), "testing procedure term text")
    ]
    
@given('Valid json payload is created where vaccination procedure term multiple instance of procedure code')
def createValidJsonPayloadWithProcedureMultipleCodings(context):
    valid_json_payload_is_created(context)
    procedures_list = VACCINATION_PROCEDURE_MAP[context.vaccine_type.upper()]
    
    if len(procedures_list) < 2:
        procedures = procedures_list  # Use all available procedures
    else:
        procedures = random.sample(procedures_list, k=2)
        
    codings = [
        Coding(
            system=proc["system"],
            code=proc["code"],
            display=proc["display"],
            extension=None
        )
        for proc in procedures
    ]
    context.immunization_object.extension[0].valueCodeableConcept.coding = codings
    
@given('Valid json payload is created where vaccination procedure term multiple instance of procedure code with different coding system')
def createValidJsonPayloadWithProcedureMultipleCodingsDifferentSystem(context):
    createValidJsonPayloadWithProcedureMultipleCodings(context)
    context.immunization_object.extension[0].valueCodeableConcept.coding[0].system = "http://example.com/different-system"
    
@given('Valid json payload is created where vaccination procedure term has one instance of procedure code with no text or value string field')
def createValidJsonPayloadWithProcedureNoTextValue(context):
    valid_json_payload_is_created(context)
    context.immunization_object.extension[0].valueCodeableConcept= build_vaccine_procedure_code(context.vaccine_type.upper(), add_extensions=False)
    

@then('The X-Request-ID and X-Correlation-ID keys in header will populate correctly')
def validateCreateHeader(context):
    assert "X-Request-ID" in context.response.request.headers, "X-Request-ID missing in headers"
    assert "X-Correlation-ID" in context.response.request.headers, "X-Correlation-ID missing in headers"
    assert context.response.request.headers["X-Request-ID"] == context.reqID, "X-Request-ID incorrect"
    assert context.response.request.headers["X-Correlation-ID"] == context.corrID, "X-Correlation-ID incorrect"    

@then('The imms event table will be populated with the correct data for created event')
def validate_imms_event_table(context):
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
        ("Operation", "CREATE", item.get("Operation")),
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
    
@then('The delta table will be populated with the correct data for created event')
def validate_imms_delta_table_by_ImmsID(context):
    create_obj = context.create_object
    item = fetch_immunization_int_delta_detail_by_immsID(context.aws_profile_name, context.ImmsID)
    assert item, f"Item not found in response for ImmsID: {context.ImmsID}"
     
    validate_imms_delta_record_with_created_event(context, create_obj, item, "CREATE")    
  

@then('The procedure term is mapped to text field in imms delta table')
def validate_procedure_term_text_in_delta_table(context):
     actual_procedure_term = get_procedure_term_text(context)
     assert actual_procedure_term == context.create_object.extension[0].valueCodeableConcept.text, f"Expected procedure term text '{context.create_object.extension[0].valueCodeableConcept.text}', but got '{actual_procedure_term}'"

@then('The procedure term is mapped to correct instance of coding display text field in imms delta table')
def validate_procedure_term_first_display_in_delta_table(context):
    actual_procedure_term = get_procedure_term_text(context)
    assert actual_procedure_term == context.create_object.extension[0].valueCodeableConcept.coding[0].display, f"Expected procedure term text '{context.create_object.extension[0].valueCodeableConcept.text}', but got '{actual_procedure_term}'"
    
@then('The procedure term is mapped to correct coding system value and display text field in imms delta table')
def validate_procedure_term_correct_coding_in_delta_table(context):
    actual_procedure_term = get_procedure_term_text(context)  
    assert actual_procedure_term == context.create_object.extension[0].valueCodeableConcept.coding[1].display, f"Expected procedure term text '{context.create_object.extension[0].valueCodeableConcept.text}', but got '{actual_procedure_term}'"
    
@then('The procedure term is mapped to correct coding display text field in imms delta table')
def validate_procedure_term_second_display_in_delta_table(context):
    actual_procedure_term = get_procedure_term_text(context)
    assert actual_procedure_term == context.create_object.extension[0].valueCodeableConcept.coding[0].display, f"Expected procedure term text '{context.create_object.extension[0].valueCodeableConcept.text}', but got '{actual_procedure_term}'"

def get_procedure_term_text(context):
    item = fetch_immunization_int_delta_detail_by_immsID(context.aws_profile_name, context.ImmsID)
    assert item, f"Item not found in response for ImmsID: {context.ImmsID}"
    
    event = item[0].get("Imms")
    assert event, "Imms field missing in items."

    procedure_term = event.get("VACCINATION_PROCEDURE_TERM")
    assert procedure_term, "Procedure term text field is missing in the delta table item." 
    
    return procedure_term
