from dataclasses import fields, is_dataclass
from logging import config
from typing import Type, Dict
import uuid
from pydantic import BaseModel
import pytest_check as check

import uuid

from src.objectModels.dataObjects import *
from src.objectModels.operation_outcome import OperationOutcome
from src.objectModels.vaccination_constants import ERROR_MAP
from utilities.helper import covert_to_expected_date_format


def find_entry_by_Imms_id(parsed_data, imms_id) -> Optional[object]:
    return next(
        (
            entry for entry in parsed_data.entry
            if entry.resource.resourceType == "Immunization" and entry.resource.id == imms_id
        ),
        None  
    )

def find_patient_by_fullurl(parsed_data) -> Optional[Entry]:
    for entry in parsed_data.entry:
        if entry.resource.resourceType == "Patient" :
            return entry
    return None


RESOURCE_MAP: Dict[str, Type[BaseModel]] = {
    "Immunization": FHIRImmunizationResponse,  
    "Patient": PatientResource, 
}

def parse_entry(entry_data: dict) -> Entry:
    resource_data = entry_data["resource"]
    resource_type = resource_data.get("resourceType", "").lower()  # ✅ Normalize case

    resource_class = RESOURCE_MAP.get(resource_type.capitalize())  # ✅ Match correct class

    if not resource_class:
        raise ValueError(f"Unsupported resourceType: {resource_type}")

    parsed_resource = resource_class.parse_obj(resource_data)
    parsed_search = Search.parse_obj(entry_data.get("search", {}))

    return Entry(
        fullUrl=entry_data.get("fullUrl"),
        resource=parsed_resource,
        search=parsed_search
    )

def validateErrorResponse(error_response, errorName: str):
    uuid_obj = uuid.UUID(error_response.id, version=4)
    check.is_true(isinstance(uuid_obj, uuid.UUID), f"Id is not UUID {error_response.id}")
    
    fields_to_compare = [
        ("ResourceType", error_response.resourceType, ERROR_MAP["Common_field"]["resourceType"]),
        ("Meta_Profile", error_response.meta.profile[0], ERROR_MAP["Common_field"]["profile"]),
        ("Coding_system",  error_response.issue[0].details.coding[0].system, ERROR_MAP["Common_field"]["system"]),
        ("Coding_Code",  error_response.issue[0].details.coding[0].code, ERROR_MAP["Common_field"]["code"]),
        ("severity",  error_response.issue[0].severity, ERROR_MAP[errorName]["severity"]),
        ("Issue_Code",  error_response.issue[0].code, ERROR_MAP[errorName]["code"]),
        ("Diagnostics",  error_response.issue[0].diagnostics, ERROR_MAP[errorName]["diagnostics"]),
    ]

    for name, expected, actual in fields_to_compare:
        check.is_true(
            expected == actual,
            f"Expected {name}: {expected}, got {actual}"
        )


def parse_FHIRImmunizationResponse(json_data: dict) -> FHIRImmunizationResponse:
    return FHIRImmunizationResponse.parse_obj(json_data)  

def parse_errorResponse(json_data: dict) -> OperationOutcome:
    return OperationOutcome.parse_obj(json_data) 

def validateToCompareRequestAndResponse(context, create_obj, created_event):
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



 