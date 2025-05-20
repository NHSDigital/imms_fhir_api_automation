from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Union

@dataclass
class Vaccine_code:
    system: str
    code: str
    display: str
    manufacturer: str

@dataclass
class Identifier_Coding:
    system: str
    code: str
    display: str
    userSelected: Optional[bool] = None
    version: Optional[str] = None

@dataclass
class Coding:
    system: str
    code: str
    display: Optional[str] = None

@dataclass
class TargetDisease:
    coding: List[Coding]
    text: Optional[str] = None

@dataclass
class ProtocolApplied:
    targetDisease: List[TargetDisease]
    doseNumberPositiveInt: int

@dataclass
class CodeDetails:
    coding: List[Coding]
    text: Optional[str] = None

@dataclass
class DoseQuantity:
    value: float
    unit: str
    system: str
    code: str

@dataclass
class CodeableConcept:
    coding: List[Coding]
    text: Optional[str] = None

@dataclass
class IType:
    coding: List[Identifier_Coding]  
    text: Optional[str] = None

@dataclass
class Period:
    start: str
    end: str

@dataclass
class Patient_Identifier:
    system: str
    value: Optional[str] = None

@dataclass
class Identifier:
    system: str
    value: Optional[str] = None 
    use: Optional[str] = None
    type: Optional[IType] = None
    period: Optional[Period] = None

@dataclass
class HumanName:
    family: str
    given: List[str]

@dataclass
class Address:
    use: str
    type: str
    text: str
    line: List[str]
    city: str
    district: str
    state: str
    postalCode: str
    country: str
    period: Dict[str, str]

@dataclass
class Practitioner:
    name: List[HumanName]
    resourceType: str = "Practitioner"
    id: str = "Pract1"

@dataclass
class Patient:
    identifier: List[Patient_Identifier]
    name: List[HumanName]
    gender: str
    birthDate: str
    address: List[Address]
    resourceType: str = "Patient"
    id: str = "Pat1"

@dataclass
class Extension:
    url: str
    valueCodeableConcept: CodeableConcept

@dataclass
class Performer:
    actor: Dict[str, Any]

@dataclass
class ReasonCode:
    coding: List[Coding]
    text: Optional[str] = None

@dataclass
class Immunization:
    contained: List[Any]
    extension: List[Extension]
    identifier: List[Identifier]
    vaccineCode: CodeDetails
    patient: Dict[str, str]
    manufacturer: Dict[str, str]
    location: Identifier_Coding
    site: CodeDetails
    route: CodeDetails
    doseQuantity: DoseQuantity
    performer: List[Performer]
    reasonCode: List[ReasonCode]
    protocolApplied: List[ProtocolApplied]
    resourceType: str = "Immunization"
    status: str = "completed"
    occurrenceDateTime: str = ""
    recorded: str = ""
    primarySource: bool = True
    lotNumber: str = ""
    expirationDate: str = ""

@dataclass
class ResponsePatient:
    reference: str
    type: str
    identifier: Patient_Identifier

@dataclass
class ImmunizationResponse:
    resourceType: str
    id: str
    extension: List[Extension]
    identifier: List[Identifier]
    status: str
    vaccineCode: CodeDetails
    patient: ResponsePatient
    occurrenceDateTime: str
    recorded: str
    lotNumber: str
    expirationDate: str
    primarySource: bool
    location: Identifier_Coding
    manufacturer: Dict[str, Any]
    site: CodeDetails
    route: CodeDetails
    doseQuantity: DoseQuantity
    performer: List[Performer]
    reasonCode: List[ReasonCode]
    protocolApplied: List[ProtocolApplied]

@dataclass
class Link:
    relation: str
    url: str

@dataclass
class Search:
    mode: str

@dataclass
class PatientResource:
    resourceType: str
    id: str
    identifier: List[Patient_Identifier]

@dataclass
class Entry:
    fullUrl: str
    resource: Union[ImmunizationResponse, PatientResource] 
    search: Search

@dataclass
class FHIRImmunizationResponse:
    resourceType: str
    type: str
    link: List[Link]
    entry: List[Entry]
    total: int

