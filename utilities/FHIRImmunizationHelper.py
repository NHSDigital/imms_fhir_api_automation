from dataclasses import fields, is_dataclass
from typing import Type, Dict
from pydantic import BaseModel
import pytest_check as check

from src.objectModels.dataObjects import *
from src.objectModels.operation_outcome import OperationOutcome


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

def validateErrorResponse(error_response, error):
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





 