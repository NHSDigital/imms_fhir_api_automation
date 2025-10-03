import time
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.config import Config
from utilities.api_fhir_immunization_helper import *
import pytest_check as check
from typing import List, Dict
from collections import Counter
from src.objectModels.api_data_objects import ImmunizationReadResponse_IntTable
from utilities.enums import *
from utilities.vaccination_constants import PROTOCOL_DISEASE_MAP

my_config = Config(
    region_name='eu-west-2',
    connect_timeout=10,  
    read_timeout=500 
)

class DynamoDBHelper:
    def __init__(self, aws_profile_name: str = None, env: str = "int"):
        self.env = env
        if aws_profile_name and aws_profile_name.strip():
            session = boto3.Session(profile_name=aws_profile_name)
            self.dynamodb = session.resource('dynamodb', config=my_config)
        else:
            self.dynamodb = boto3.resource('dynamodb', config=my_config)

    def get_events_table(self):
        return self.dynamodb.Table(f'imms-{self.env}-imms-events')

    def get_delta_table(self):
        return self.dynamodb.Table(f'imms-{self.env}-delta')
    
    def get_batch_audit_table(self):
        return self.dynamodb.Table(f'immunisation-batch-{self.env}-audit-table')


def fetch_immunization_events_detail(aws_profile_name:str, ImmsID: str, env:str,):
    db = DynamoDBHelper(aws_profile_name, env)
    tableImmsEvent = db.get_events_table()

    queryFetch = f"Immunization#{ImmsID}"

    response = tableImmsEvent.get_item(Key={'PK': queryFetch})
    print(f"\n Imms Event response is {response} \n")

    return response

def fetch_items_by_attribute(
    aws_profile_name: str,
    env: str,
    table_getter: callable,
    attribute_name: str,
    attribute_value: str,
    max_retries: int = 3,
    wait_seconds: int = 3
):
    db = DynamoDBHelper(aws_profile_name, env)
    table = table_getter(db)

    for attempt in range(max_retries):
        response = table.scan(
            FilterExpression=Attr(attribute_name).eq(attribute_value)
        )

        items = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression=Attr(attribute_name).eq(attribute_value),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))

        if items:
            break

        if attempt < max_retries - 1:
            print(f"\n Waiting for DynamoDB table to update... (attempt {attempt + 1})")
            time.sleep(wait_seconds)

    print(f"\n Scan response for {attribute_name} = {attribute_value}: {items}\n")
    return items


def fetch_immunization_int_delta_detail_by_immsID(aws_profile_name:str, ImmsID: str, env:str, max_retries: int = 3, wait_seconds: int = 3):
    items = fetch_items_by_attribute(
        aws_profile_name=aws_profile_name,
        env=env,
        table_getter=DynamoDBHelper.get_delta_table,
        attribute_name="ImmsID",
        attribute_value=ImmsID,
        max_retries=max_retries,
        wait_seconds=wait_seconds
        )

    return items

def fetch_batch_audit_table_detail(aws_profile_name:str, filename: str, env:str, max_retries: int = 3, wait_seconds: int = 3):
    items = fetch_items_by_attribute(
        aws_profile_name=aws_profile_name,
        env=env,
        table_getter=DynamoDBHelper.get_batch_audit_table,
        attribute_name="filename",
        attribute_value=filename,
        max_retries=max_retries,
        wait_seconds=wait_seconds
    )

    return items
    
def parse_imms_int_imms_event_response(resource: dict) -> ImmunizationReadResponse_IntTable:
    contained_raw = resource.get("contained", [])
    parsed_contained = []

    for item in contained_raw:
        if item.get("resourcetype") == "patient":
            parsed_contained.append(Patient.parse_obj(item))
        elif item.get("resourcetype") == "practitioner":
            parsed_contained.append(Practitioner.parse_obj(item))
        else:
            parsed_contained.append(item)  # fallback or raise error

    resource["contained"] = parsed_contained
    return ImmunizationReadResponse_IntTable.parse_obj(resource)

def validate_imms_delta_record_with_created_event(context, create_obj, item, event_type, action_flag):
    event = item[0].get("Imms")
    assert event, "Imms field missing in items."
    
    fields_to_compare = [
        ("Operation", event_type.upper(), item[0].get("Operation")),
        ("SupplierSystem", context.supplier_name.lower(), item[0].get("SupplierSystem").lower()),
        ("VaccineType", f"{context.vaccine_type.lower()}", item[0].get("VaccineType").lower()),
        ("Source", "IEDS", item[0].get("Source")),
        ("CONVERSION_ERRORS", [], event.get("CONVERSION_ERRORS")),
        ("PERSON_FORENAME", create_obj.contained[1].name[0].given[0], event.get("PERSON_FORENAME")),
        ("PERSON_SURNAME", create_obj.contained[1].name[0].family, event.get("PERSON_SURNAME")),
        ("NHS_NUMBER", create_obj.contained[1].identifier[0].value, event.get("NHS_NUMBER")),
        ("PERSON_DOB", create_obj.contained[1].birthDate.replace("-", ""), event.get("PERSON_DOB")),
        ("PERSON_POSTCODE", create_obj.contained[1].address[0].postalCode, event.get("PERSON_POSTCODE")),
        ("PERSON_GENDER_CODE", GenderCode[(create_obj.contained[1].gender)].value, event.get("PERSON_GENDER_CODE")),
        ("VACCINATION_PROCEDURE_CODE", create_obj.extension[0].valueCodeableConcept.coding[0].code, event.get("VACCINATION_PROCEDURE_CODE")),        
        ("VACCINATION_PROCEDURE_TERM", create_obj.extension[0].valueCodeableConcept.coding[0].extension[0].valueString, event.get("VACCINATION_PROCEDURE_TERM")),
        ("VACCINE_PRODUCT_TERM", create_obj.vaccineCode.coding[0].extension[0].valueString, event.get("VACCINE_PRODUCT_TERM")),
        ("VACCINE_PRODUCT_CODE", create_obj.vaccineCode.coding[0].code, event.get("VACCINE_PRODUCT_CODE")),
        ("VACCINE_MANUFACTURER", create_obj.manufacturer["display"] , event.get("VACCINE_MANUFACTURER")),
        ("BATCH_NUMBER", create_obj.lotNumber, event.get("BATCH_NUMBER")),
        ("RECORDED_DATE", create_obj.recorded[:10].replace("-", ""), event.get("RECORDED_DATE")),
        ("EXPIRY_DATE", create_obj.expirationDate.replace("-", ""), event.get("EXPIRY_DATE")),
        ("DOSE_SEQUENCE", str(create_obj.protocolApplied[0].doseNumberPositiveInt), event.get("DOSE_SEQUENCE")),
        ("DOSE_UNIT_TERM", create_obj.doseQuantity.unit , event.get("DOSE_UNIT_TERM")),
        ("DOSE_UNIT_CODE", create_obj.doseQuantity.code, event.get("DOSE_UNIT_CODE")),         
        ("SITE_OF_VACCINATION_TERM", create_obj.site.coding[0].extension[0].valueString, event.get("SITE_OF_VACCINATION_TERM")),
        ("SITE_OF_VACCINATION_CODE", create_obj.site.coding[0].code, event.get("SITE_OF_VACCINATION_CODE")),        
        ("DOSE_AMOUNT", create_obj.doseQuantity.value , float(event.get("DOSE_AMOUNT")) ),
        ("PRIMARY_SOURCE", str(create_obj.primarySource).upper(), event.get("PRIMARY_SOURCE")),
        ("ROUTE_OF_VACCINATION_TERM", create_obj.route.coding[0].extension[0].valueString, event.get("ROUTE_OF_VACCINATION_TERM")),
        ("ROUTE_OF_VACCINATION_CODE", create_obj.route.coding[0].code, event.get("ROUTE_OF_VACCINATION_CODE")),
        ("ACTION_FLAG", action_flag, event.get("ACTION_FLAG")),
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
        


def get_all_term_text(context):
    item = fetch_immunization_int_delta_detail_by_immsID(context.aws_profile_name, context.ImmsID, context.S3_env)
    assert item, f"Item not found in response for ImmsID: {context.ImmsID}"
    
    event = item[0].get("Imms")
    assert event, "Imms field missing in items."

    assert "VACCINATION_PROCEDURE_TERM" in event, "Procedure term text field is missing in the delta table item."
    procedure_term = event.get("VACCINATION_PROCEDURE_TERM")

    assert "VACCINE_PRODUCT_TERM" in event, "Product term text field is missing in the delta table item."
    product_term = event.get("VACCINE_PRODUCT_TERM")

    assert "SITE_OF_VACCINATION_TERM" in event, "Site of vaccination term text field is missing in the delta table item."
    site_term = event.get("SITE_OF_VACCINATION_TERM")

    assert "ROUTE_OF_VACCINATION_TERM" in event, "Route of vaccination term text field is missing in the delta table item."
    route_term = event.get("ROUTE_OF_VACCINATION_TERM")      
    
    return {
        "procedure_term" : procedure_term ,
        "product_term" : product_term,
        "site_term" : site_term,
        "route_term" : route_term
         }

def get_all_the_vaccination_codes(list_items):
    return [
        Coding(
            system=item["system"],
            code=item["code"],
            display=item["display"],
            extension=None
        )
        for item in list_items
    ]
    
def validate_audit_table_record(context, item, expected_status: str, expected_error_detail: str = None):
    check.is_true(
        item.get("status") == expected_status,
        f"Expected status {expected_status}, got '{item.get('status')}'"
    )

    expected_queue = f"{context.supplier_name}_{context.vaccine_type}"
    check.is_true(
        item.get("queue_name") == expected_queue,
        f"Expected queue_name '{expected_queue}', got '{item.get('queue_name')}'"
    )

    check.is_true(
        item.get("filename") == context.filename,
        f"Expected filename '{context.filename}', got '{item.get('filename')}'"
    )

    check.is_true(
        "timestamp" in item,
        "processed_timestamp not found in item"
    )

    check.is_true(
        item.get("error_detail") == expected_error_detail,
        f"Expected error_detail {expected_error_detail}, but got: {item.get('error_detail')}"
    )
    
def validate_imms_delta_record_with_batch_record(context, batch_record, item, event_type, action_flag):
    event = item[0].get("Imms")
    assert event, "Imms field missing in items."
    
    fields_to_compare = [
        ("Operation", event_type.upper(), item[0].get("Operation")),
        ("SupplierSystem", context.supplier_name.lower(), item[0].get("SupplierSystem").lower()),
        ("VaccineType", f"{context.vaccine_type.lower()}", item[0].get("VaccineType").lower()),
        ("Source", "IEDS", item[0].get("Source")),
        ("CONVERSION_ERRORS", [], event.get("CONVERSION_ERRORS")),
        ("PERSON_FORENAME", batch_record["PERSON_FORENAME"], event.get("PERSON_FORENAME")),
        ("PERSON_SURNAME", batch_record["PERSON_SURNAME"], event.get("PERSON_SURNAME")),
        ("NHS_NUMBER", batch_record["NHS_NUMBER"], event.get("NHS_NUMBER")),
        ("PERSON_DOB", batch_record["PERSON_DOB"], event.get("PERSON_DOB")),
        ("PERSON_POSTCODE", batch_record["PERSON_POSTCODE"], event.get("PERSON_POSTCODE")),
        ("PERSON_GENDER_CODE", batch_record["PERSON_GENDER_CODE"], event.get("PERSON_GENDER_CODE")),
        ("VACCINATION_PROCEDURE_CODE", batch_record["VACCINATION_PROCEDURE_CODE"], event.get("VACCINATION_PROCEDURE_CODE")),        
        ("VACCINATION_PROCEDURE_TERM", batch_record["VACCINATION_PROCEDURE_TERM"], event.get("VACCINATION_PROCEDURE_TERM")),
        ("VACCINE_PRODUCT_TERM", batch_record["VACCINE_PRODUCT_TERM"], event.get("VACCINE_PRODUCT_TERM")),
        ("VACCINE_PRODUCT_CODE", batch_record["VACCINE_PRODUCT_CODE"], event.get("VACCINE_PRODUCT_CODE")),
        ("VACCINE_MANUFACTURER", batch_record["VACCINE_MANUFACTURER"] , event.get("VACCINE_MANUFACTURER")),
        ("BATCH_NUMBER", batch_record["BATCH_NUMBER"], event.get("BATCH_NUMBER")),
        ("RECORDED_DATE", batch_record["RECORDED_DATE"], event.get("RECORDED_DATE")),
        ("EXPIRY_DATE", batch_record["EXPIRY_DATE"], event.get("EXPIRY_DATE")),
        ("DOSE_SEQUENCE", batch_record["DOSE_SEQUENCE"], event.get("DOSE_SEQUENCE")),
        ("DOSE_UNIT_TERM", batch_record["DOSE_UNIT_TERM"] , event.get("DOSE_UNIT_TERM")),
        ("DOSE_UNIT_CODE", batch_record["DOSE_UNIT_CODE"], event.get("DOSE_UNIT_CODE")),         
        ("SITE_OF_VACCINATION_TERM", batch_record["SITE_OF_VACCINATION_TERM"], event.get("SITE_OF_VACCINATION_TERM")),
        ("SITE_OF_VACCINATION_CODE", batch_record["SITE_OF_VACCINATION_CODE"], event.get("SITE_OF_VACCINATION_CODE")),        
        ("DOSE_AMOUNT", float(batch_record["DOSE_AMOUNT"]) , float(event.get("DOSE_AMOUNT"))),
        ("PRIMARY_SOURCE", str(batch_record["PRIMARY_SOURCE"]).upper(), event.get("PRIMARY_SOURCE")),
        ("ROUTE_OF_VACCINATION_TERM", batch_record["ROUTE_OF_VACCINATION_TERM"], event.get("ROUTE_OF_VACCINATION_TERM")),
        ("ROUTE_OF_VACCINATION_CODE", batch_record["ROUTE_OF_VACCINATION_CODE"], event.get("ROUTE_OF_VACCINATION_CODE")),
        ("ACTION_FLAG", action_flag, event.get("ACTION_FLAG")),
        ("DATE_AND_TIME", batch_record["DATE_AND_TIME"], event.get("DATE_AND_TIME")),
        ("UNIQUE_ID", batch_record["UNIQUE_ID"], event.get("UNIQUE_ID")),
        ("UNIQUE_ID_URI", batch_record["UNIQUE_ID_URI"], event.get("UNIQUE_ID_URI")),
        ("PERFORMING_PROFESSIONAL_SURNAME", batch_record["PERFORMING_PROFESSIONAL_SURNAME"], event.get("PERFORMING_PROFESSIONAL_SURNAME")),  
        ("PERFORMING_PROFESSIONAL_FORENAME", batch_record["PERFORMING_PROFESSIONAL_FORENAME"], event.get("PERFORMING_PROFESSIONAL_FORENAME")),
        ("LOCATION_CODE", batch_record["LOCATION_CODE"], event.get("LOCATION_CODE")),
        ("LOCATION_CODE_TYPE_URI", batch_record["LOCATION_CODE_TYPE_URI"], event.get("LOCATION_CODE_TYPE_URI")),
        ("SITE_CODE_TYPE_URI", batch_record["SITE_CODE_TYPE_URI"], event.get("SITE_CODE_TYPE_URI")),
        ("SITE_CODE", batch_record["SITE_CODE"], event.get("SITE_CODE")),
        ("INDICATION_CODE", batch_record["INDICATION_CODE"] , event.get("INDICATION_CODE")),  
    ]

    for name, expected, actual in fields_to_compare:
        check.is_true(
                expected == actual,
                f"for ImmsID {context.ImmsID}  -- Expected {name}: {expected}, Actual {actual}"
            )  
        
def validateToCompareBatchRecordWithEventTableRecord(context, batch_record, created_event):
    response_patient, response_practitioner = extract_patient_and_practitioner(created_event.contained)

    check.is_true(response_patient is not None, "Patient not found in contained resources")
    check.is_true(response_practitioner is not None, "Practitioner not found in contained resources")

    created_occurrence_date = batch_record["DATE_AND_TIME"]
    trimmed_date = created_occurrence_date[:-2]
    expected_occurrenceDateTime = f'{covert_to_expected_date_format(trimmed_date)}+00:00'
    expected_recorded = covert_to_expected_date_format(batch_record["RECORDED_DATE"])
    actual_occurrenceDateTime = covert_to_expected_date_format(created_event.occurrenceDateTime)
    actual_recorded = covert_to_expected_date_format(created_event.recorded)
        
    fields_to_compare = [
        ("patient.reference", "#Patient1", created_event.patient.reference),
        ("Id", context.ImmsID, created_event.id),
        ("resourceType", "Immunization", created_event.resourceType),        
        ("identifier.system", batch_record["UNIQUE_ID_URI"], created_event.identifier[0].system),
        ("identifier.value", batch_record["UNIQUE_ID"], created_event.identifier[0].value),
        ("status", "completed", created_event.status),                  
        ("occurrenceDateTime", expected_occurrenceDateTime, actual_occurrenceDateTime),
        ("Recorded", expected_recorded, actual_recorded),
        ("primarySource", str(batch_record["PRIMARY_SOURCE"]).lower(), str(created_event.primarySource).lower()),
        ("location.vale", batch_record["LOCATION_CODE"], created_event.location.identifier.value),
        ("location.system", batch_record["LOCATION_CODE_TYPE_URI"], created_event.location.identifier.system),
        ("manufacturer", batch_record["VACCINE_MANUFACTURER"] , created_event.manufacturer["display"]),
        ("lotNumber", batch_record["BATCH_NUMBER"], created_event.lotNumber),
        ("expirationDate", format_date_yyyymmdd(batch_record["EXPIRY_DATE"]), created_event.expirationDate),       
        ("doseQuantity.value", float(batch_record["DOSE_AMOUNT"]), created_event.doseQuantity.value),
        ("doseQuantity.term",  batch_record["DOSE_UNIT_TERM"], created_event.doseQuantity.unit),
        ("doseQuantity.code", batch_record["DOSE_UNIT_CODE"], created_event.doseQuantity.code),
        ("doseQuantity.system", "http://snomed.info/sct", created_event.doseQuantity.system),        
        ("protocolApplied", True, compare_protocol_codings_to_reference(created_event.protocolApplied,PROTOCOL_DISEASE_MAP.get(context.vaccine_type.upper(), []))),
        ("protocolApplied.doseNumberPositiveInt", 1, created_event.protocolApplied[0].doseNumberPositiveInt),
       # ("reasonCode.coding.code", batch_record["INDICATION_CODE"] , created_event.reasonCode[0].coding[0].code),  
        #("reasonCode.coding.system", "http://snomed.info/sct" , created_event.reasonCode[0].coding[0].system),  
       # ("reasonCode.text", created_event.reasonCode[0].text, created_event.reasonCode[0].text),  
        ("Patient.id", "Patient1", response_patient.id),
        ("Patient.identifier.value", batch_record["NHS_NUMBER"], response_patient.identifier[0].value),
        ("Patient.identifier.system", "https://fhir.nhs.uk/Id/nhs-number", response_patient.identifier[0].system),
        ("Patient.birthdate", format_date_yyyymmdd(batch_record["PERSON_DOB"]), response_patient.birthDate),
        ("Patient.Gender", GenderCode(batch_record["PERSON_GENDER_CODE"]).name.lower(), response_patient.gender),
        ("Patient.name.family", batch_record["PERSON_SURNAME"], response_patient.name[0].family),
        ("Patient.name.given", batch_record["PERSON_FORENAME"], response_patient.name[0].given[0]),
        ("Patient.address.postalCode", batch_record["PERSON_POSTCODE"], response_patient.address[0].postalCode),
        ("Practitioner.id", "Practitioner1", response_practitioner.id),
        ("Practitioner.name.family", batch_record["PERFORMING_PROFESSIONAL_SURNAME"], response_practitioner.name[0].family),
        ("Practitioner.name.given", batch_record["PERFORMING_PROFESSIONAL_FORENAME"], response_practitioner.name[0].given[0]),
        ("extension.url", "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-VaccinationProcedure", created_event.extension[0].url),
        ("extension.valueCodeableConcept.coding.code", batch_record["VACCINATION_PROCEDURE_CODE"], created_event.extension[0].valueCodeableConcept.coding[0].code),
        ("extension.valueCodeableConcept.coding.system", "http://snomed.info/sct", created_event.extension[0].valueCodeableConcept.coding[0].system),
        ("extension.valueCodeableConcept.coding.extension.valueString", batch_record["VACCINATION_PROCEDURE_TERM"], created_event.extension[0].valueCodeableConcept.coding[0].display),
        ("site.coding.code", batch_record["SITE_OF_VACCINATION_CODE"], created_event.site.coding[0].code),
        ("site.coding.system", "http://snomed.info/sct", created_event.site.coding[0].system),
        ("site.coding.extension.display", batch_record["SITE_OF_VACCINATION_TERM"], created_event.site.coding[0].display),
        ("route.coding.code", batch_record["ROUTE_OF_VACCINATION_CODE"], created_event.route.coding[0].code),
        ("route.coding.system", "http://snomed.info/sct", created_event.route.coding[0].system),
        ("route.coding.display", batch_record["ROUTE_OF_VACCINATION_TERM"], created_event.route.coding[0].display),
        ("performer.actor.type", "Organization", created_event.performer[0].actor.type),
        ("performer.actor.reference", "#Practitioner1", created_event.performer[1].actor.reference),
        ("performer.actor.identifier.value", batch_record["SITE_CODE"], created_event.performer[0].actor.identifier.value),
        ("performer.actor.identifier.system", batch_record["SITE_CODE_TYPE_URI"], created_event.performer[0].actor.identifier.system),        
        ("vaccineCode.coding.code", batch_record["VACCINE_PRODUCT_CODE"], created_event.vaccineCode.coding[0].code),
        ("vaccineCode.coding.system", "http://snomed.info/sct", created_event.vaccineCode.coding[0].system),
        ("vaccineCode.coding.extension.valueString", batch_record["VACCINE_PRODUCT_TERM"], created_event.vaccineCode.coding[0].display)
    ]

    for name, expected, actual in fields_to_compare:
        check.is_true(
                expected == actual,
                f"Expected {name}: {expected}, Actual {actual}"
            )   
        

def normalize_coding(coding) -> Dict[str, str]:
    """Extracts and normalizes a coding dict from a Coding object."""
    return {
        "system": coding.system,
        "code": coding.code,
        "display": coding.display
    }

def extract_protocol_codings(protocol_applied) -> List[Dict[str, str]]:
    """Flattens all codings from protocolApplied into a list of normalized dicts."""
    codings = []
    for protocol in protocol_applied:
        for disease in protocol.targetDisease:
            for coding in disease.coding:
                codings.append(normalize_coding(coding))
    return codings

def compare_protocol_codings_to_reference(protocol_applied: List[ProtocolApplied], reference_codings: List[Dict[str, str]]) -> bool:
    extracted = extract_protocol_codings(protocol_applied)
    
    # Convert both lists to Counter of sorted tuples for order-insensitive comparison
    extracted_counter = Counter(tuple(sorted(d.items())) for d in extracted)
    reference_counter = Counter(tuple(sorted(d.items())) for d in reference_codings)

    return extracted_counter == reference_counter

def extract_patient_and_practitioner(contained):
    patient = None
    practitioner = None

    for resource in contained:
        if resource.resourceType == "Patient":
            patient = resource
        elif resource.resourceType == "Practitioner":
            practitioner = resource

    return patient, practitioner

