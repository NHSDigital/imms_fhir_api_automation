from src.objectModels.dataObjects import *
from src.objectModels.vaccination_constants import *
from datetime import datetime, timedelta, timezone
from dataclasses import is_dataclass, fields
from typing import Any
import random
import uuid

def build_vaccine_procedure_extension(vaccine_type: str, text: str = "") -> Extension:
    try:
        selected_vaccine_procedure = random.choice(VACCINATION_PROCEDURE_MAP[vaccine_type.upper()])
    except KeyError:
        raise ValueError(f"Unsupported vaccine type: {vaccine_type}")

    return Extension(
        url="https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-VaccinationProcedure",
        valueCodeableConcept=CodeableConcept(
            coding=[selected_vaccine_procedure],
            text=text
        )
    )


def build_coding_concept(coding_map: List[Any], text: str = "") -> CodeDetails:
    selected = random.choice(coding_map)
    
    return CodeDetails(
        coding=[selected],
        text=text
    )


def build_location_identifier() -> Identifier_Coding:
    coding_list = [
        Identifier_Coding(
            system="http://terminology.hl7.org/CodeSystem/v2-0203",
            version="Test version",
            code="123456",
            display="Test display",
            userSelected=True
        )
    ]

    return {
        "identifier": Identifier(
            value="X99999",
            system="https://fhir.nhs.uk/Id/ods-organization-code",
            use="official",
            type=Type(
                coding=coding_list,
                text="test string Location"
            ),
            period=Period(
                start="2000-01-01",
                end="2025-01-01"
            )
        )
    }

def build_protocol_applied(vaccine_type: str, dose_number: int = 1, text: str = "") -> List[ProtocolApplied]:
    selected_disease = random.choice(PROTOCOL_DISEASE_MAP.get(vaccine_type.upper(), []))

    if not selected_disease:
        raise ValueError(f"Unsupported vaccine type: {vaccine_type}")

    return [
        ProtocolApplied(
            targetDisease=[TargetDisease(coding=[selected_disease], text=text)],  
            doseNumberPositiveInt=dose_number
        )
    ]

def get_vaccine_details(vaccine_type: str, vacc_text: str = "", lot_number: str = "", expiry_date: str ="") -> Dict[str, Any]:
    selected_vaccine = random.choice(VACCINE_CODE_MAP[vaccine_type.upper()])

    vaccine_code = CodeDetails(
        coding=[Coding(
            system=selected_vaccine.system,
            code=selected_vaccine.code,
            display=selected_vaccine.display
        )],  # Only include relevant Coding attributes
        text=vacc_text
    )

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

def build_performer() -> List[Performer]:
    return [
        Performer(actor={"reference": "#Pract1"}),
        Performer(actor={
            "type": "Organization",
            "display": "UNIVERSITY HOSPITAL OF WALES",
            "identifier": Identifier(
                value="B0C4P",
                system="https://fhir.nhs.uk/Id/ods-organization-code",
                use="usual",
                type=Type(
                    coding=[
                        Identifier_Coding(
                            system="http://terminology.hl7.org/CodeSystem/v2-0203",
                            code="123456",
                            display="Test display performer",
                            version="Test version performer",
                            userSelected=True
                        )
                    ],
                    text="test string performer"
                ),
                period=Period(
                    start="2000-01-01",
                    end="2025-01-01"
                )
            )
        })
    ]

def get_dateTime(date: str = '') -> str:
    if not date:
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
    return date

def get_unique_identifier()-> List[Dict[str, Any]]:
    return [Identifier(system="https://supplierABC/identifiers/vacc", value=str(uuid.uuid4()))]

def build_reason_code(reason_code_map: List[Any], text: str = "") -> List[ReasonCode]:
    selected = random.choice(reason_code_map)

    return [
        ReasonCode(
            coding=[Coding(
                system=selected.system,
                code=selected.code,
                display=selected.display
            )],
            text=text
        )
    ]

def dose_quantity_selection() -> DoseQuantity:
    return DoseQuantity(**random.choice(DOSE_QUANTITY_MAP))

def clean_dataclass(obj):
    """Recursively cleans a dataclass instance, removing None, empty lists/dicts, and 'null' values, while keeping it as an object."""
    
    if is_dataclass(obj):
        obj_dict = {f.name: clean_dataclass(getattr(obj, f.name)) for f in fields(obj)}
        obj_dict = {k: v for k, v in obj_dict.items() if v not in (None, "null", {}, [], "")}
        
        return obj.__class__(**obj_dict) if obj_dict else None  

    elif isinstance(obj, list):
        return [clean_dataclass(item) for item in obj if item not in (None, "null", {}, [], "")]

    elif isinstance(obj, dict):
        return {k: clean_dataclass(v) for k, v in obj.items() if v not in (None, "null", {}, [], "")}

    return obj

def deep_asdict(obj):
    """Recursively converts dataclass objects to dictionaries."""
    if is_dataclass(obj):
        return {k: deep_asdict(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [deep_asdict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: deep_asdict(v) for k, v in obj.items()}
    else:
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
        doseQuantity=dose_quantity_selection(),
        performer = build_performer(),
        reasonCode = build_reason_code(REASON_CODE_MAP),
        protocolApplied = build_protocol_applied(vaccine_type)
)