from dataclasses import is_dataclass
from typing import get_type_hints

from src.objectModels.dataObjects import *

# Mapping for top-level resource types.
RESOURCE_TYPE_MAP = {
    # For top‑level deserialization you might want to support these:
    "Patient": Patient,
    "Practitioner": Practitioner,
    "ImmunizationResponse": ImmunizationResponse,
    # Do not include ResponsePatient here, so that nested patient objects use 
    # the declared type (ResponsePatient) even if resourceType is "Patient".
}

def parse_dataclass(cls, data, ignore_resource_type: bool = False, is_top_level: bool = True):
    from dataclasses import is_dataclass
from typing import get_type_hints

# Top-level mapping. (Do not use ResponsePatient here so that nested patient objects get overridden.)
RESOURCE_TYPE_MAP = {
    "Patient": Patient,
    "Practitioner": Practitioner,
    "ImmunizationResponse": ImmunizationResponse,
    # ... add others as needed.
}

def parse_dataclass(cls, data, ignore_resource_type: bool = False, is_top_level: bool = True):
    """
    Recursively parses a JSON dictionary (or list) into a dataclass instance.
    
    If a key is missing in the JSON response, it is simply omitted
    (so that it’s not passed into the constructor).
    
    For classes like CodeDetails, ReasonCode, and TargetDisease, if "text" is missing
    it is forced to "".
    
    Special cases are defined for Coding and Identifier_Coding.
    
    IMPORTANT:
      - At the top level (is_top_level=True) the RESOURCE_TYPE_MAP is applied.
      - For nested objects (is_top_level=False), if the JSON shows "resourceType": "Patient"
        we force the expected type to be ResponsePatient.
      - Instead of calling the normal constructor (which would require all required fields),
        we bypass __init__ by creating the instance with object.__new__(cls)
        and then setting only the parsed keys.
    
    Args:
        cls: The target dataclass type (or generic type such as List[…]).
        data: The JSON data (dict, list, or primitive) to parse.
        ignore_resource_type: When True, any "resourceType" present is ignored.
        is_top_level: When True, signals the top-level call.
    
    Returns:
        An instance of cls populated with the keys present in data.
    """
    if isinstance(data, dict):
        # For nested objects: if not top-level or ignoring resourceType, and data shows Patient,
        # then force use of ResponsePatient.
        if (not is_top_level or ignore_resource_type) and data.get("resourceType") == "Patient":
            try:
                from src.objectModels.dataObjects import ResponsePatient
                cls = ResponsePatient
            except ImportError:
                pass
        # Otherwise, at top level use resourceType mapping if available.
        elif is_top_level and not ignore_resource_type and "resourceType" in data:
            res_type = data["resourceType"]
            if cls.__name__ != "ResponsePatient" and res_type in RESOURCE_TYPE_MAP:
                cls = RESOURCE_TYPE_MAP[res_type]
        
        if not isinstance(cls, type):
            return data

        # Special case for Coding.
        if cls.__name__ == "Coding":
            return cls(
                system=data.get("system", ""),
                code=data.get("code", ""),
                display=data.get("display", "")
            )
        # Special case for Identifier_Coding.
        if cls.__name__ == "Identifier_Coding":
            if "identifier" in data and isinstance(data["identifier"], dict):
                inner = data["identifier"]
                if "type" in inner and isinstance(inner["type"], dict):
                    type_data = inner["type"]
                    coding_list = type_data.get("coding", [])
                    if coding_list and isinstance(coding_list, list):
                        coding_data = coding_list[0]
                        instance = object.__new__(cls)
                        setattr(instance, "system", coding_data.get("system", ""))
                        setattr(instance, "code", coding_data.get("code", ""))
                        setattr(instance, "display", coding_data.get("display", ""))
                        setattr(instance, "userSelected", coding_data.get("userSelected"))
                        setattr(instance, "version", coding_data.get("version"))
                        return instance
            instance = object.__new__(cls)
            setattr(instance, "system", data.get("system", ""))
            setattr(instance, "code", data.get("code", ""))
            setattr(instance, "display", data.get("display", ""))
            setattr(instance, "userSelected", data.get("userSelected"))
            setattr(instance, "version", data.get("version"))
            return instance

        # For general dataclasses, retrieve the field type hints and recursively parse.
        field_types = get_type_hints(cls)
        field_values = {}
        for key, field_type in field_types.items():
            if key in data:
                # For the field "patient", force ignore_resource_type for nested parsing.
                if key == "patient":
                    field_values[key] = parse_dataclass(field_type, data[key], ignore_resource_type=True, is_top_level=False)
                else:
                    field_values[key] = parse_dataclass(field_type, data[key], is_top_level=False)
        # For classes where missing "text" should become "", add it if not present.
        if cls.__name__ in ["CodeDetails", "ReasonCode", "TargetDisease"]:
            if "text" not in field_values:
                field_values["text"] = ""
        # Bypass __init__ by creating an instance using object.__new__ and setting attributes.
        instance = object.__new__(cls)
        for key, value in field_values.items():
            setattr(instance, key, value)
        return instance

    elif isinstance(data, list):
        # For lists, try to get the element type.
        element_type = None
        try:
            element_type = cls.__args__[0]
        except (AttributeError, IndexError):
            element_type = None
        return [parse_dataclass(element_type, item, is_top_level=False) for item in data]

    # Base case for primitives.
    return data


def find_entry_by_Imms_id(parsed_data, target_id):
    return next((entry for entry in parsed_data.entry if entry.resource.id == target_id), None)

 