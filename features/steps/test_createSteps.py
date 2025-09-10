from src.dynamoDB.dynamoDBHelper import *
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from utilities.FHIRImmunizationHelper import *
from utilities.enums import ActionFlag
from utilities.getHeader import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
import logging
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from features.steps.common_steps import *


logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)


scenarios("create.feature")

@given('Valid json payload is created where vaccination terms has text field populated')
def createValidJsonPayloadWithProcedureText(context):
    valid_json_payload_is_created(context)
    context.immunization_object.extension = [build_vaccine_procedure_extension(context.vaccine_type.upper(), "testing procedure term text")]
    vaccine_details = get_vaccine_details(context.vaccine_type.upper(), "testing product term text")
    context.immunization_object.vaccineCode = vaccine_details["vaccine_code"]
    context.immunization_object.site = build_site_route(random.choice(SITE_MAP), "testing site text")
    context.immunization_object.route = build_site_route(random.choice(ROUTE_MAP), "testing route text")

    
@given('Valid json payload is created where vaccination terms has multiple instances of coding')
def createValidJsonPayloadWithProcedureMultipleCodings(context):
    valid_json_payload_is_created(context)
    procedures_list = get_all_the_vaccination_codes(VACCINATION_PROCEDURE_MAP[context.vaccine_type.upper()])
    product_list = get_all_the_vaccination_codes(VACCINE_CODE_MAP[context.vaccine_type.upper()])
    
    context.immunization_object.extension[0].valueCodeableConcept.coding = procedures_list
    context.immunization_object.vaccineCode.coding = product_list
    
@given('Valid json payload is created where vaccination terms has multiple instance of coding with different coding system')
def createValidJsonPayloadWithProcedureMultipleCodingsDifferentSystem(context):
    createValidJsonPayloadWithProcedureMultipleCodings(context)
    site_list = get_all_the_vaccination_codes(SITE_MAP)
    route_list = get_all_the_vaccination_codes(ROUTE_MAP)
    context.immunization_object.site.coding = site_list
    context.immunization_object.route.coding = route_list

    context.immunization_object.extension[0].valueCodeableConcept.coding[0].system = "http://example.com/different-system"
    context.immunization_object.vaccineCode.coding[0].system = "http://example.com/different-system"
    context.immunization_object.site.coding[0].system = "http://example.com/different-system"
    context.immunization_object.route.coding[0].system = "http://example.com/different-system"
    
@given('Valid json payload is created where vaccination terms has one instance of coding with no text or value string field')
def createValidJsonPayloadWithProcedureNoTextValue(context):
    valid_json_payload_is_created(context)
    context.immunization_object.extension[0].valueCodeableConcept= build_vaccine_procedure_code(context.vaccine_type.upper(), add_extensions=False)
    vaccine_details = get_vaccine_details(context.vaccine_type.upper(), add_extensions=False)
    context.immunization_object.vaccineCode = vaccine_details["vaccine_code"]

    context.immunization_object.site = build_site_route(random.choice(SITE_MAP), add_extensions=False)
    context.immunization_object.route = build_site_route(random.choice(ROUTE_MAP), add_extensions=False)


@given('Valid json payload is created where vaccination terms has no text or value string or display field')
def createValidJsonPayloadWithProcedureNoTextValueDisplay(context):
    valid_json_payload_is_created(context)
    context.immunization_object.extension[0].valueCodeableConcept.coding[0].extension = None
    context.immunization_object.extension[0].valueCodeableConcept.coding[0].display = None
    context.immunization_object.extension[0].valueCodeableConcept.text = None  
    context.immunization_object.vaccineCode.coding[0].extension = None
    context.immunization_object.vaccineCode.coding[0].display = None
    context.immunization_object.vaccineCode.text = None      
    context.immunization_object.site.coding[0].extension = None
    context.immunization_object.site.coding[0].display = None
    context.immunization_object.site.text = None      
    context.immunization_object.route.coding[0].extension = None
    context.immunization_object.route.coding[0].display = None
    context.immunization_object.route.text = None          


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
        ("IdentifierPK", f"{create_obj.identifier[0].system}#{create_obj.identifier[0].value}", item.get("IdentifierPK")),
        ("Operation", Operation.created.value, item.get("Operation")),
        ("PatientPK", f"Patient#{context.patient.identifier[0].value}", item.get("PatientPK")),
        ("PatientSK", f"{context.vaccine_type}#{context.ImmsID}", item.get("PatientSK")),
        ("SupplierSystem", context.supplier_name.lower(), item.get("SupplierSystem").lower()),        
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
     
    validate_imms_delta_record_with_created_event(context, create_obj, item, Operation.created.value, ActionFlag.created.value)    
  
@then('The terms are mapped to the respective text fields in imms delta table')
def validate_procedure_term_text_in_delta_table(context):
     actual_terms = get_all_term_text(context)
     assert actual_terms["procedure_term"] == context.create_object.extension[0].valueCodeableConcept.text, f"Expected procedure term '{context.create_object.extension[0].valueCodeableConcept.text}', but got '{actual_terms['procedure_term']}'"
     assert actual_terms["product_term"] == context.create_object.vaccineCode.text, f"Expected product term '{context.create_object.vaccineCode.text}', but got '{actual_terms['product_term']}'"
     assert actual_terms["site_term"] == context.create_object.site.text, f"Expected site of vaccination term '{context.create_object.site.text}', but got '{actual_terms['site_term']}'"
     assert actual_terms["route_term"] == context.create_object.route.text, f"Expected route of vaccination term '{context.create_object.route.text}', but got '{actual_terms['route_term']}'"
     print(f"\n The delta table fields covered are VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM\n")
     
@then('The terms are mapped to first instance of coding.display fields in imms delta table')
def validate_procedure_term_first_display_in_delta_table(context):
    actual_terms = get_all_term_text(context)
    assert actual_terms["procedure_term"] == context.create_object.extension[0].valueCodeableConcept.coding[0].display, f"Expected procedure term '{context.create_object.extension[0].valueCodeableConcept.coding[0].display}', but got '{actual_terms['procedure_term']}'"
    assert actual_terms["product_term"] == context.create_object.vaccineCode.coding[0].display, f"Expected product term '{context.create_object.vaccineCode.coding[0].display}', but got '{actual_terms['product_term']}'"
    
@then('The terms are mapped to correct instance of coding.display fields in imms delta table')
def validate_procedure_term_correct_coding_in_delta_table(context):
    actual_terms = get_all_term_text(context)  
    assert actual_terms["procedure_term"] == context.create_object.extension[0].valueCodeableConcept.coding[1].display, f"Expected procedure term text '{context.create_object.extension[0].valueCodeableConcept.coding[1].display}', but got '{actual_terms['procedure_term']}'"
    assert actual_terms["product_term"] == context.create_object.vaccineCode.coding[1].display, f"Expected product term '{context.create_object.vaccineCode.coding[1].display}', but got '{actual_terms['product_term']}'"
    assert actual_terms["site_term"] == context.create_object.site.coding[1].display, f"Expected site of vaccination term '{context.create_object.site.coding[1].display}', but got '{actual_terms['site_term']}'"
    assert actual_terms["route_term"] == context.create_object.route.coding[1].display, f"Expected route of vaccination term '{context.create_object.route.coding[1].display}', but got '{actual_terms['route_term']}'"
    
@then('The terms are mapped to correct coding.display fields in imms delta table')
def validate_procedure_term_second_display_in_delta_table(context):
    actual_terms = get_all_term_text(context)
    assert actual_terms["procedure_term"] == context.create_object.extension[0].valueCodeableConcept.coding[0].display, f"Expected procedure term text '{context.create_object.extension[0].valueCodeableConcept.coding[0].display}', but got '{actual_terms['procedure_term']}'"
    assert actual_terms["product_term"] == context.create_object.vaccineCode.coding[0].display, f"Expected product term text '{context.create_object.vaccineCode.coding[0].display}', but got '{actual_terms['product_term']}'"
    assert actual_terms["site_term"] == context.create_object.site.coding[0].display, f"Expected site of vaccination term text '{context.create_object.site.coding[0].display}', but got '{actual_terms['site_term']}'"
    assert actual_terms["route_term"] == context.create_object.route.coding[0].display, f"Expected route of vaccination term text '{context.create_object.route.coding[0].display}', but got '{actual_terms['route_term']}'"

@then('The terms are blank in imms delta table')
def validate_procedure_term_blank_in_delta_table(context):
    actual_terms = get_all_term_text(context)
    assert actual_terms["procedure_term"] == "", f"Expected procedure term text to be blank, but got '{actual_terms['procedure_term']}'"
    assert actual_terms["product_term"] == "", f"Expected product term text to be blank, but got '{actual_terms['product_term']}'"
    assert actual_terms["site_term"] == "", f"Expected site of vaccination term text to be blank, but got '{actual_terms['site_term']}'"
    assert actual_terms["route_term"] == "", f"Expected route of vaccination term text to be blank, but got '{actual_terms['route_term']}'"




