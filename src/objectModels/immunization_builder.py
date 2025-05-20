from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import random
import uuid
from src.objectModels.dataObjects import *
from src.objectModels.vaccination_constants import *

def build_vaccine_procedure_extension(vaccine_type: str, text: str = None) -> Extension:
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

def build_location_identifier() -> Location:
    return Location(
        identifier=LocationIdentifier(
            system="https://fhir.nhs.uk/Id/ods-organization-code",
            value="X99999"
        )
    )

def get_vaccine_details(vaccine_type: str, vacc_text: str = None, lot_number: str = "", expiry_date: str = "") -> Dict[str, Any]:
    selected_vaccine = random.choice(VACCINE_CODE_MAP[vaccine_type.upper()])  

    vaccine_code = CodeableConcept(
        coding=[Coding(
            system=selected_vaccine["system"],  
            code=selected_vaccine["code"], 
            display=selected_vaccine["display"]
        )],
        text=vacc_text
    )

    manufacturer = {"display": selected_vaccine["manufacturer"]}  

    if not lot_number:
        lot_number = str(random.randint(100000, 999999))

    if not expiry_date:
        future_date = datetime.now() + timedelta(days=365 * 2)  
        expiry_date = future_date.strftime('%Y-%m-%d')

    return {
        "vaccine_code": vaccine_code,
        "manufacturer": manufacturer,
        "lotNumber": lot_number,
        "expiryDate": expiry_date
    }


def build_performer() -> List[Performer]:
    return [
        Performer(actor=Reference(reference="#Pract1", type="Practitioner")),
        Performer(actor=Reference(
            reference="Organization/B0C4P",  
            type="Organization",
            identifier=Identifier(
                value="B0C4P",
                system="https://fhir.nhs.uk/Id/ods-organization-code",
                use="usual",
                type=CodeableConcept(
                    coding=[
                        Coding(
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
            ),
            display="UNIVERSITY HOSPITAL OF WALES"
        ))
    ]

def remove_empty_fields(data):
    """ Recursively removes fields with empty values from a dictionary. """
    if isinstance(data, dict):
        return {k: remove_empty_fields(v) for k, v in data.items() if v != ""}
    elif isinstance(data, list):
        return [remove_empty_fields(item) for item in data]
    else:
        return data
    
def create_immunization_object(patient: Patient, vaccine_type: str) -> Immunization:
    practitioner = Practitioner(
        resourceType="Practitioner",  # ✅ Explicitly set resourceType
        id="Pract1",  
        name=[HumanName(family="Furlong", given=["Darren"])]
    )
    extension = [build_vaccine_procedure_extension(vaccine_type.upper())]
    vaccine_details = get_vaccine_details(vaccine_type)

    return Immunization(
        resourceType="Immunization",
        contained=[practitioner, patient],
        extension=extension,
        identifier=[Identifier(system="https://supplierABC/identifiers/vacc", value=str(uuid.uuid4()))],
        vaccineCode=vaccine_details["vaccine_code"], 
        patient=Reference(reference=f"#{patient.id}", type="Patient"),  
        occurrenceDateTime=datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        recorded=datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        manufacturer=vaccine_details["manufacturer"],
        location=build_location_identifier(),
        lotNumber=vaccine_details["lotNumber"],
        status="completed",
        primarySource= True,
        expirationDate=vaccine_details["expiryDate"],
        site=CodeableConcept(coding=[random.choice(SITE_MAP)]),
        route=CodeableConcept(coding=[random.choice(ROUTE_MAP)]),
        doseQuantity=DoseQuantity(**random.choice(DOSE_QUANTITY_MAP)),
        performer=build_performer(),
        reasonCode=[CodeableConcept(coding=[random.choice(REASON_CODE_MAP)])],
        protocolApplied=[ProtocolApplied(targetDisease=[CodeableConcept(coding=[random.choice(PROTOCOL_DISEASE_MAP.get(vaccine_type.upper(), []))])], doseNumberPositiveInt=1)]
    )
