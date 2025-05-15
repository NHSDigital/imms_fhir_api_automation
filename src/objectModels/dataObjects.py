from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass 
class Vaccine_code:
    system: str
    code: str
    display: str
    manufacturer : str

@dataclass
class Coding:
    system: str
    code: str
    display: str

@dataclass
class CodeableConcept:
    coding: List[Coding]

@dataclass
class Identifier:
    system: str
    value: str
    use: Optional[str] = None  
    type: Optional[Dict[str, Any]] = None  
    period: Optional[Dict[str, str]] = None

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
    resourceType: str = "Practitioner"
    id: str = "Pract1"
    name: List[HumanName] = field(default_factory=list)

@dataclass
class Patient:
    resourceType: str = "Patient"
    id: str = "Pat1"
    identifier: List[Identifier] = field(default_factory=list)
    name: List[HumanName] = field(default_factory=list)
    gender: str = "unknown"
    birthDate: str = "1980-01-01"
    address: List[Address] = field(default_factory=list)

@dataclass
class Extension:
    url: str
    valueCodeableConcept: CodeableConcept

@dataclass
class Performer:
    actor: Dict[str, Any]

@dataclass
class Immunization:
    resourceType: str = "Immunization"
    contained: List[Any] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)
    identifier: List[Identifier] = field(default_factory=list)
    status: str = "completed"
    vaccineCode: CodeableConcept = None
    patient: Dict[str, str] = field(default_factory=dict)
    occurrenceDateTime: str = ""
    recorded: str = ""
    primarySource: bool = True
    manufacturer: Dict[str, str] = field(default_factory=dict)
    location: Dict[str, Any] = field(default_factory=dict)
    lotNumber: str = ""
    expirationDate: str = ""
    site: CodeableConcept = None
    route: CodeableConcept = None
    doseQuantity: Dict[str, Any] = field(default_factory=dict)
    performer: List[Performer] = field(default_factory=list)
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    protocolApplied: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ImmunizationResponse:
    resourceType: str =" "
    id: str =" "
    extension: List[Extension] = field(default_factory=list)
    identifier: List[Identifier] = field(default_factory=list)
    status: str = " "
    vaccineCode: List[CodeableConcept] = field(default_factory=list)
    patient: Patient = None
    occurrenceDateTime: str =" "
    recorded: str = " "
    lotNumber: str =" "
    expirationDate: str =" "
    primarySource: bool = True
    location: Dict[str, Any] = field(default_factory=list)
    manufacturer: Dict[str, Any] = field(default_factory=list)    
    site: CodeableConcept = field(default_factory=list)  
    route: CodeableConcept = field(default_factory=list)  
    doseQuantity: Dict[str, Any] = field(default_factory=dict)
    performer: List[Performer] = field(default_factory=list)
    reasonCode: List[CodeableConcept] = field(default_factory=list)
    protocolApplied: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class Link:
    relation: str
    url: str
@dataclass
class Entry:
    fullUrl: str
    resource: ImmunizationResponse
    search: Dict[str, str]

@dataclass
class FHIRImmunizationResponse:
    resourceType: str
    type: str
    link: List[Link]
    entry: List[Entry]
    total: int
