from typing_extensions import get_type_hints

from src.objectModels.dataObjects import Coding

def parse_dataclass(cls, data):
    """Recursively parse JSON dictionary into a dataclass object."""
    if isinstance(data, dict):
        if isinstance(cls, type):
            field_types = get_type_hints(cls)  # Get type hints safely
        else:
            return data  # Return raw data if cls isn't a class

        # Special handling for `Coding` class
        if cls == Coding:
            return Coding(
                system=data.get("system", ""),
                code=data.get("code", ""),
                display=data.get("display", "")
            )

        field_values = {
            key: parse_dataclass(field_types.get(key, type(value)), value)
            for key, value in data.items()
            if key in field_types
        }
        return cls(**field_values)

    elif isinstance(data, list):
        # Ensure `cls.__args__` exists before accessing it
        element_type = getattr(cls, '__args__', [None])[0]
        if isinstance(element_type, type):  # Only proceed if it's a class
            return [parse_dataclass(element_type, item) for item in data]

    return data

def find_entry_by_Imms_id(parsed_data, target_id):
    return next((entry for entry in parsed_data.entry if entry.resource.id == target_id), None)

 