from typing import  List, Literal, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class ExtensionItem(BaseModel):
    url: str
    valueString: Optional[str] = None
    valueId: Optional[str] = None


class Coding(BaseModel):
    extension: Optional[List[ExtensionItem]] = None
    system: str
    code: str
    display: Optional[str] = None

class CodeableConcept(BaseModel):
    coding: List[Coding]
    text: Optional[str] = None 

class Period(BaseModel):
    start: str
    end: str

class Identifier(BaseModel):
    system: str
    value: Optional[str] = None
    use: Optional[str] = None
    type: Optional[CodeableConcept] = None
    period: Optional[Period] = None

class Reference(BaseModel):
    reference: str
    type: str
    identifier: Optional[Identifier] = None

class HumanName(BaseModel):
    family: str
    given: List[str]

class Address(BaseModel):
    use: str
    type: str
    text: str
    line: List[str]
    city: str
    district: str
    state: str
    postalCode: str
    country: str
    period: Period

class Practitioner(BaseModel):
    resourceType: str = "Practitioner"
    id: str
    name: List[HumanName]

class Patient(BaseModel):
    resourceType: str 
    id: str
    identifier: List[Identifier]
    name: List[HumanName]
    gender: str
    birthDate: str
    address: List[Address]

class Extension(BaseModel):
    url: str
    valueCodeableConcept: CodeableConcept

class Performer(BaseModel):
    actor: Reference  # Updated to match FHIR structure

class ReasonCode(BaseModel):
    coding: List[Coding]
    text: Optional[str] = None

class DoseQuantity(BaseModel):
    value: float
    unit: str
    system: str
    code: str

class ProtocolApplied(BaseModel):
    targetDisease: List[CodeableConcept]
    doseNumberPositiveInt: int

class LocationIdentifier(BaseModel):
    system: str
    value: str

class Location(BaseModel):
    identifier: LocationIdentifier

class Immunization(BaseModel):
    resourceType: str = "Immunization"
    contained: List[Any]
    extension: List[Extension]
    identifier: List[Identifier]
    status: str = "completed"
    vaccineCode: CodeableConcept  # Fixed type
    patient: Reference  # Fixed type
    manufacturer: Dict[str, str]
    location: Location  
    site: CodeableConcept
    route: CodeableConcept
    doseQuantity: DoseQuantity
    performer: List[Performer]
    reasonCode: List[ReasonCode]
    protocolApplied: List[ProtocolApplied]
    occurrenceDateTime: str = ""
    recorded: str = ""
    primarySource: bool = True
    lotNumber: str = ""
    expirationDate: str = ""

    class Config:
        orm_mode = True 

class ResponseActorOrganization(BaseModel):
    type: str = "Organization"
    display: Optional[str] = None
    identifier: Identifier  

class ResponsePerformer(BaseModel):
    actor: ResponseActorOrganization


class Link(BaseModel):
    relation: str
    url: str

class Search(BaseModel):
    mode: str

class PatientIdentifier(BaseModel):
    system: str
    value: Optional[str] = None

class ResponsePatient(BaseModel):
    reference: str
    type: str
    identifier: PatientIdentifier
   

class ImmunizationResponse(BaseModel):
    resourceType:  Literal["Immunization"]
    id: str
    extension: List[Extension]
    identifier: List[Identifier]
    status: str
    vaccineCode: CodeableConcept
    patient: ResponsePatient
    occurrenceDateTime: str
    recorded: str
    lotNumber: str
    expirationDate: str
    primarySource: bool
    location: Location
    manufacturer: Dict[str, Any]
    site: CodeableConcept
    route: CodeableConcept
    doseQuantity: DoseQuantity
    performer: List[ResponsePerformer]
    reasonCode: List[ReasonCode]
    protocolApplied: List[ProtocolApplied]

class PatientResource(BaseModel):
    resourceType: Literal["Patient"]
    id: str
    identifier: List[PatientIdentifier]

class Entry(BaseModel):
    fullUrl: str
    resource:Annotated[
        Union[ImmunizationResponse, PatientResource],
        Field(discriminator="resourceType")]
    search: Dict[str, str]

class FHIRImmunizationResponse(BaseModel):
    resourceType: str
    type: Optional[str] = None  
    link: Optional[List[Link]] = []  
    entry: Optional[List[Entry]] = []  
    total: Optional[int] = None