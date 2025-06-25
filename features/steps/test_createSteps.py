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

    fields_to_compare = [
        ("Operation", "CREATE", item[0].get("Operation")),
        ("SupplierSystem", "Postman_Auth", item[0].get("SupplierSystem")),
        ("VaccineType", f"{context.vaccine_type.lower()}", item[0].get("VaccineType")),
        ("Source", "IEDS", item[0].get("Source")),
    ]

    for name, expected, actual in fields_to_compare:
        check.is_true(
                expected == actual,
                f"Expected {name}: {expected}, Actual {actual}"
            )
        
    event = item[0].get("Imms")
    assert event, "Imms field missing in items."
    
    fields_to_compare = [
        ("CONVERSION_ERRORS", [], event.get("CONVERSION_ERRORS")),
        ("PERSON_FORENAME", create_obj.contained[1].name[0].given[0], event.get("PERSON_FORENAME")),
        ("PERSON_SURNAME", create_obj.contained[1].name[0].family, event.get("PERSON_SURNAME")),
        ("NHS_NUMBER", create_obj.contained[1].identifier[0].value, event.get("NHS_NUMBER")),
        ("PERSON_DOB", create_obj.contained[1].birthDate.replace("-", ""), event.get("PERSON_DOB")),
        ("PERSON_POSTCODE", create_obj.contained[1].address[0].postalCode, event.get("PERSON_POSTCODE")),
        ("PERSON_GENDER_CODE", gender_map.get(create_obj.contained[1].gender), event.get("PERSON_GENDER_CODE")),
        ("VACCINATION_PROCEDURE_CODE", create_obj.extension[0].valueCodeableConcept.coding[0].code, event.get("VACCINATION_PROCEDURE_CODE")),        
        ("VACCINATION_PROCEDURE_TERM", create_obj.extension[0].valueCodeableConcept.coding[0].extension[0].valueString, event.get("VACCINATION_PROCEDURE_TERM")),
        ("VACCINE_PRODUCT_TERM", create_obj.vaccineCode.coding[0].extension[0].valueString, event.get("VACCINE_PRODUCT_TERM")),
        ("VACCINE_PRODUCT_CODE", create_obj.vaccineCode.coding[0].code, event.get("VACCINE_PRODUCT_CODE")),
        ("VACCINE_MANUFACTURER", create_obj.manufacturer["display"] , event.get("VACCINE_MANUFACTURER")),
        ("BATCH_NUMBER", create_obj.lotNumber, event.get("BATCH_NUMBER")),
        ("RECORDED_DATE", create_obj.recorded[:10].replace("-", ""), event.get("RECORDED_DATE")),
        ("EXPIRY_DATE", create_obj.expirationDate.replace("-", ""), event.get("EXPIRY_DATE")),
        ("DOSE_SEQUENCE", "1", event.get("DOSE_SEQUENCE")),
        ("DOSE_UNIT_TERM", create_obj.doseQuantity.unit , event.get("DOSE_UNIT_TERM")),
        ("DOSE_UNIT_CODE", create_obj.doseQuantity.code, event.get("DOSE_UNIT_CODE")),         
        ("SITE_OF_VACCINATION_TERM", create_obj.site.coding[0].extension[0].valueString, event.get("SITE_OF_VACCINATION_TERM")),
        ("SITE_OF_VACCINATION_CODE", create_obj.site.coding[0].code, event.get("SITE_OF_VACCINATION_CODE")),        
        ("DOSE_AMOUNT", create_obj.doseQuantity.value , float(event.get("DOSE_AMOUNT")) ),
        ("PRIMARY_SOURCE", create_obj.primarySource, event.get("PRIMARY_SOURCE")),
        ("ROUTE_OF_VACCINATION_TERM", create_obj.route.coding[0].extension[0].valueString, event.get("ROUTE_OF_VACCINATION_TERM")),
        ("ROUTE_OF_VACCINATION_CODE", create_obj.route.coding[0].code, event.get("ROUTE_OF_VACCINATION_CODE")),
        ("ACTION_FLAG", "NEW", event.get("ACTION_FLAG")),
        ("DATE_AND_TIME", iso_to_compact(create_obj.occurrenceDateTime), event.get("DATE_AND_TIME")),
        ("UNIQUE_ID", create_obj.identifier[0].value, event.get("UNIQUE_ID")),
        ("UNIQUE_ID_URI", create_obj.identifier[0].system, event.get("UNIQUE_ID_URI")),
        ("PERFORMING_PROFESSIONAL_SURNAME", create_obj.contained[0].name[0].family, event.get("PERFORMING_PROFESSIONAL_SURNAME")),  
        ("PERFORMING_PROFESSIONAL_FORENAME", create_obj.contained[0].name[0].given[0], event.get("PERFORMING_PROFESSIONAL_FORENAME")),
        ("LOCATION_CODE", create_obj.location.identifier.value, event.get("LOCATION_CODE")),
        ("LOCATION_CODE_TYPE_URI", create_obj.location.identifier.system, event.get("LOCATION_CODE_TYPE_URI")),
        ("SITE_CODE_TYPE_URI", create_obj.location.identifier.system, event.get("SITE_CODE_TYPE_URI")),
        ("SITE_CODE", create_obj.performer[1].actor.identifier.value, event.get("SITE_CODE")),
        ("INDICATION_CODE", create_obj.reasonCode[0].coding[0].code , event.get("INDICATION_CODE")),  
    ]

    for name, expected, actual in fields_to_compare:
        check.is_true(
                expected == actual,
                f"Expected {name}: {expected}, Actual {actual}"
            )    


gender_map = {
    "male": "1",
    "female": "2",
    "unknown": "0",
    "other": "9"
}

