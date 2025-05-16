from src.objectModels.dataObjects import *
from src.objectModels.vaccination_constants import *
from datetime import datetime, timedelta, timezone
from dataclasses import is_dataclass, fields
from typing import Any
import random
import uuid

def build_vaccine_procedure_extension(vaccine_type: str) -> Extension:
    try:
        selected_vaccine_procedure = random.choice(VACCINATION_PROCEDURE_MAP[vaccine_type.upper()])
    except KeyError:
        raise ValueError(f"Unsupported vaccine type: {vaccine_type}")

    return Extension(
        url="https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-VaccinationProcedure",
        valueCodeableConcept=CodeableConcept(
            coding=[
                Coding(
                    system=selected_vaccine_procedure.system,
                    code=selected_vaccine_procedure.code,
                    display=selected_vaccine_procedure.display
                )
            ]
        )
    )


def build_coding_concept(coding_map: List[Any]) -> Dict[str, Any]:
    selected = random.choice(coding_map)
    return {
        "coding": [
            {
                "system": selected.system,
                "code": selected.code,
                "display": selected.display
            }
        ]
    }


def build_location_identifier() -> dict:
    return {
        "identifier": Identifier(
            value="X99999",
            system="https://fhir.nhs.uk/Id/ods-organization-code",
            use="official",
            type={
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                    "version": "Test version",
                    "code": "123456",
                    "display": "Test display",
                    "userSelected": True
                }],
                "text": "test string Location"
            },
            period={
                "start": "2000-01-01",
                "end": "2025-01-01"
            }
        )
    }

def build_protocol_applied(vaccine_type: str, dose_number: int = 1) -> List[Dict[str, Any]]:
    selected_disease = random.choice(PROTOCOL_DISEASE_MAP[vaccine_type.upper()])
    
    return [
        {
            "targetDisease": [
                {
                    "coding": [
                        {
                            "system": selected_disease.system,
                            "code": selected_disease.code,
                            "display": selected_disease.display
                        }
                    ]
                }
            ],
            "doseNumberPositiveInt": dose_number
        }
    ]

def get_vaccine_details(vaccine_type: str, lot_number: str = "", expiry_date: str ="") -> Dict[str, Any]:
    selected_vaccine = random.choice(VACCINE_CODE_MAP[vaccine_type.upper()])

    vaccine_code = {
        "coding": [
            {
                "system": selected_vaccine.system,
                "code": selected_vaccine.code,
                "display": selected_vaccine.display
            }
        ]
    }

    manufacturer = {"display": selected_vaccine.manufacturer}

    if not lot_number:
        lot_number = str(random.randint(100000, 999999))

    if not expiry_date:
        future_date = datetime.now() + timedelta(days=365 * 2)  # 2 years from today
        expiry_date = future_date.strftime('%Y-%m-%d')

    return {
        "vaccine_code": vaccine_code,
        "manufacturer": manufacturer,
        "lotNumber": lot_number,
        "expiryDate": expiry_date
    }

def build_performer()-> List[Dict[str, Any]]:
    return [
            Performer(actor={"reference": "#Pract1"}),
            Performer(actor={
                "type": "Organization",
                "display": "UNIVERSITY HOSPITAL OF WALES",
                "identifier": Identifier(
                    value="B0C4P",
                    system="https://fhir.nhs.uk/Id/ods-organization-code",
                    use="usual",
                    type={  
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "123456",
                                "display": "Test display performer",
                                "version": "Test version performer",
                                "userSelected": True
                            }
                        ],
                        "text": "test string performer"
                    },
                    period={"start": "2000-01-01", "end": "2025-01-01"}
                )
            })
        ]

def get_dateTime(date: str = '') -> str:
    if not date:
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
    return date

def get_unique_identifier()-> List[Dict[str, Any]]:
    return [Identifier(system="https://supplierABC/identifiers/vacc", value=str(uuid.uuid4()))]

def build_reason_code(reason_code_map: List[Any]) -> List[ReasonCode]:
    selected = random.choice(reason_code_map)
    return [
        ReasonCode(
            coding=[
                Coding(
                    system=selected.system,
                    code=selected.code,
                    display=selected.display
                )
            ]
        )
    ]

def to_clean_dict(obj) -> Any:
    """Recursively clean dataclass objects, removing None & empty values, ensuring correct `reasonCode` serialization."""

    if is_dataclass(obj):
        result = {}

        for f in fields(obj):
            value = getattr(obj, f.name)
            cleaned_value = to_clean_dict(value)  # Recursively clean

            # Ensure we filter out empty structures AFTER processing
            if cleaned_value not in (None, [], {}, "", "null"):
                result[f.name] = cleaned_value

        # ✅ Fix reasonCode serialization issue: Ensure it remains a list
        if isinstance(result.get("reasonCode"), dict):  
            result["reasonCode"] = [result["reasonCode"]]  # Force list correction

        return result if result else None  # Ensure empty objects aren't retained

    elif isinstance(obj, list):
        cleaned_list = [to_clean_dict(item) for item in obj if item not in (None, {}, [], "", "null")]
        return cleaned_list if cleaned_list else None  # Remove empty lists

    elif isinstance(obj, dict):
        cleaned_dict = {k: to_clean_dict(v) for k, v in obj.items() if v not in (None, [], {}, "", "null")}
        return cleaned_dict if cleaned_dict else None  # Remove empty dictionaries

    else:
       return obj if obj not in (None, "", [], {}, "null") else None

def clean_dataclass(obj):
    """Cleans a dataclass instance without converting it to a dictionary."""
    if not is_dataclass(obj):
        return obj  # Return object as-is if it's not a dataclass

    for f in fields(obj):
        value = getattr(obj, f.name)

        # Remove None or empty values
        if value is None or (isinstance(value, list) and not value) or (isinstance(value, dict) and not value):
            setattr(obj, f.name, None)  # Set empty values to None
        
        # Recursively clean nested dataclass objects
        if is_dataclass(value):
            setattr(obj, f.name, clean_dataclass(value))
        elif isinstance(value, list):  # Clean list elements recursively
            setattr(obj, f.name, [clean_dataclass(item) for item in value if item is not None])
        elif isinstance(value, dict):  # Clean dictionary values recursively
            setattr(obj, f.name, {k: clean_dataclass(v) for k, v in value.items() if v is not None})

    return obj

def create_immunization_object(patient: Patient, vaccine_type: str) -> Immunization:
    practitioner = Practitioner(name=[HumanName(family="Furlong", given=["Darren"])])
    extension = [build_vaccine_procedure_extension(vaccine_type.upper())]
    vaccine_details = get_vaccine_details(vaccine_type)
    return Immunization(
        contained=[practitioner, patient],
        extension=extension,
        identifier=get_unique_identifier(),
        vaccineCode=vaccine_details["vaccine_code"],
        patient={"reference": f"#{patient.id}"},
        occurrenceDateTime=get_dateTime(),
        recorded=get_dateTime(),
        manufacturer=vaccine_details["manufacturer"],
        location = build_location_identifier(),
        lotNumber=vaccine_details["lotNumber"],
        expirationDate=vaccine_details["expiryDate"],
        site=build_coding_concept(SITE_MAP),
        route=build_coding_concept(ROUTE_MAP),
        doseQuantity=DOSE_QUANTITY_MAP,
        performer = build_performer(),
        reasonCode = build_reason_code(REASON_CODE_MAP),
        protocolApplied = build_protocol_applied(vaccine_type)
)