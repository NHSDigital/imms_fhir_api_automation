import time
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.config import Config
from utilities.FHIRImmunizationHelper import *
import pytest_check as check

from src.objectModels.dataObjects import ImmunizationIntTable

my_config = Config(
    region_name='eu-west-2',
    connect_timeout=10,  
    read_timeout=500 
)

class DynamoDBHelper:
    def __init__(self, aws_profile_name: str = None):
        if aws_profile_name and aws_profile_name.strip():
            session = boto3.Session(profile_name=aws_profile_name)
            self.dynamodb = session.resource('dynamodb', config=my_config)
        else:
            self.dynamodb = boto3.resource('dynamodb', config=my_config)

    def get_events_table(self):
        return self.dynamodb.Table('imms-int-imms-events')

    def get_delta_table(self):
        return self.dynamodb.Table('imms-int-delta')


def fetch_immunization_events_detail(aws_profile_name:str, ImmsID: str):
    db = DynamoDBHelper(aws_profile_name)
    tableImmsEvent = db.get_events_table()

    queryFetch = f"Immunization#{ImmsID}"

    response = tableImmsEvent.get_item(Key={'PK': queryFetch})
    print(f"\n Imms Event response is {response} \n")

    return response
    
def parse_imms_int_imms_event_response(json_data: dict) -> ImmunizationIntTable:
    return ImmunizationIntTable.parse_obj(json_data)  


def fetch_immunization_int_delta_detail_by_immsID(aws_profile_name:str, ImmsID: str, max_retries: int = 3, wait_seconds: int = 3):
    db = DynamoDBHelper(aws_profile_name)
    tableImmsDelta = db.get_delta_table()

    for attempt in range(max_retries):
        response = tableImmsDelta.scan(
            FilterExpression=Attr('ImmsID').eq(ImmsID)
        )

        items = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            response = tableImmsDelta.scan(
                FilterExpression=Attr('ImmsID').eq(ImmsID),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))

        if not items and attempt < max_retries - 1:
            time.sleep(wait_seconds)   
            print("\n Waiting for DynamoDB Delta table to update...")         

    print(f"\n Delta table response is {items} \n")

    return items

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
        ("PERSON_GENDER_CODE", gender_map.get(create_obj.contained[1].gender), event.get("PERSON_GENDER_CODE")),
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
    item = fetch_immunization_int_delta_detail_by_immsID(context.aws_profile_name, context.ImmsID)
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