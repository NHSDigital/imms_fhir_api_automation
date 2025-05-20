from dataclasses import fields, is_dataclass
from typing import Type, TypeVar, get_args, get_origin, Union, List, Dict

from src.objectModels.dataObjects import *

def find_entry_by_Imms_id(parsed_data, imms_id) -> Optional[object]:
    return next(
        (
            entry for entry in parsed_data.entry
            if entry.resource.resourceType == "Immunization" and entry.resource.id == imms_id
        ),
        None  
    )

def find_patient_by_fullurl(parsed_data, expected_fullurl: str) -> Optional[Entry]:
    for entry in parsed_data.entry:
        if entry.resource.resourceType == "Patient" and entry.fullUrl == expected_fullurl:
            return entry
    return None

T = TypeVar("T")

RESOURCE_MAP: Dict[str, Type] = {
    "Immunization": ImmunizationResponse,
    "Patient": PatientResource
}

def from_dict(data_class: Type[T], data: dict) -> T:
    """Recursively converts a dict into a dataclass object."""
    if not is_dataclass(data_class):
        return data

    kwargs = {}
    for f in fields(data_class):
        val = data.get(f.name)
        if val is None:
            kwargs[f.name] = None
            continue

        f_type = f.type
        origin = get_origin(f_type)

        if origin in (list, List):
            inner_type = get_args(f_type)[0]
            kwargs[f.name] = [from_dict(inner_type, i) for i in val]
        elif origin is Union:
            for arg in get_args(f_type):
                if arg is type(None):
                    continue
                try:
                    kwargs[f.name] = from_dict(arg, val)
                    break
                except Exception:
                    continue
        elif is_dataclass(f_type):
            kwargs[f.name] = from_dict(f_type, val)
        else:
            kwargs[f.name] = val

    return data_class(**kwargs)

def parse_entry(entry_data: dict) -> Entry:
    resource_data = entry_data["resource"]
    resource_type = resource_data.get("resourceType")

    resource_class = RESOURCE_MAP.get(resource_type)
    if not resource_class:
        raise ValueError(f"Unsupported resourceType: {resource_type}")

    parsed_resource = from_dict(resource_class, resource_data)
    parsed_search = from_dict(Search, entry_data.get("search", {}))

    return Entry(
        fullUrl=entry_data.get("fullUrl"),
        resource=parsed_resource,
        search=parsed_search
    )

def parse_FHIRImmunizationResponse(json_data: dict) -> FHIRImmunizationResponse:
    parsed_links = [from_dict(Link, link) for link in json_data.get("link", [])]
    parsed_entries = [parse_entry(entry) for entry in json_data.get("entry", [])]

    return FHIRImmunizationResponse(
        resourceType=json_data.get("resourceType"),
        type=json_data.get("type"),
        link=parsed_links,
        entry=parsed_entries,
        total=json_data.get("total")
    )

 