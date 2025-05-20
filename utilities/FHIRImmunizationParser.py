from dataclasses import fields, is_dataclass
from typing import Type, TypeVar, get_args, get_origin, Union, List, Dict

from src.objectModels.dataObjects import *

# # Mapping for top-level resource types.
# RESOURCE_TYPE_MAP = {
#     # For top‑level deserialization you might want to support these:
#     "Patient": Patient,
#     "Practitioner": Practitioner,
#     "ImmunizationResponse": ImmunizationResponse,
# }

# def parse_dataclass(cls, data, ignore_resource_type: bool = False, is_top_level: bool = True):
#     if isinstance(data, dict):
#         # For nested objects: if not top-level or ignoring resourceType, and data shows Patient,
#         # then force use of ResponsePatient.
#         if (not is_top_level or ignore_resource_type) and data.get("resourceType") == "Patient":
#             try:
#                 cls = ResponsePatient
#             except ImportError:
#                 pass
#         # Otherwise, at top level use resourceType mapping if available.
#         elif is_top_level and not ignore_resource_type and "resourceType" in data:
#             res_type = data["resourceType"]
#             if cls.__name__ != "ResponsePatient" and res_type in RESOURCE_TYPE_MAP:
#                 cls = RESOURCE_TYPE_MAP[res_type]
        
#         if not isinstance(cls, type):
#             return data

#         # Special case for Coding.
#         if cls.__name__ == "Coding":
#             return cls(
#                 system=data.get("system", ""),
#                 code=data.get("code", ""),
#                 display=data.get("display", "")
#             )
#         # Special case for Identifier_Coding.
#         if cls.__name__ == "Identifier_Coding":
#             if "identifier" in data and isinstance(data["identifier"], dict):
#                 inner = data["identifier"]
#                 if "type" in inner and isinstance(inner["type"], dict):
#                     type_data = inner["type"]
#                     coding_list = type_data.get("coding", [])
#                     if coding_list and isinstance(coding_list, list):
#                         coding_data = coding_list[0]
#                         instance = object.__new__(cls)
#                         setattr(instance, "system", coding_data.get("system", ""))
#                         setattr(instance, "code", coding_data.get("code", ""))
#                         setattr(instance, "display", coding_data.get("display", ""))
#                         setattr(instance, "userSelected", coding_data.get("userSelected"))
#                         setattr(instance, "version", coding_data.get("version"))
#                         return instance
#             instance = object.__new__(cls)
#             setattr(instance, "system", data.get("system", ""))
#             setattr(instance, "code", data.get("code", ""))
#             setattr(instance, "display", data.get("display", ""))
#             setattr(instance, "userSelected", data.get("userSelected"))
#             setattr(instance, "version", data.get("version"))
#             return instance

#         # For general dataclasses, retrieve the field type hints and recursively parse.
#         field_types = get_type_hints(cls)
#         field_values = {}
#         for key, field_type in field_types.items():
#             if key in data:
#                 # For the field "patient", force ignore_resource_type for nested parsing.
#                 if key == "patient":
#                     field_values[key] = parse_dataclass(field_type, data[key], ignore_resource_type=True, is_top_level=False)
#                 else:
#                     field_values[key] = parse_dataclass(field_type, data[key], is_top_level=False)
#         # For classes where missing "text" should become "", add it if not present.
#         if cls.__name__ in ["CodeDetails", "ReasonCode", "TargetDisease"]:
#             if "text" not in field_values:
#                 field_values["text"] = ""
#         # Bypass __init__ by creating an instance using object.__new__ and setting attributes.
#         instance = object.__new__(cls)
#         for key, value in field_values.items():
#             setattr(instance, key, value)
#         return instance

#     elif isinstance(data, list):
#         # For lists, try to get the element type.
#         element_type = None
#         try:
#             element_type = cls.__args__[0]
#         except (AttributeError, IndexError):
#             element_type = None
#         return [parse_dataclass(element_type, item, is_top_level=False) for item in data]

#     return data


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

 