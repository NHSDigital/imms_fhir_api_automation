from dataclasses import fields, is_dataclass
from typing import Type, TypeVar, get_args, get_origin, Union, List, Dict
from pydantic import BaseModel

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


def parse_FHIRImmunizationResponse(json_data: dict) -> FHIRImmunizationResponse:
    return FHIRImmunizationResponse.parse_obj(json_data)  

def parse_errorResponse(json_data: dict) -> OperationOutcome:
    return OperationOutcome.parse_obj(json_data) 





 