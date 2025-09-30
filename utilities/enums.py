from enum import Enum

class Operation(Enum):
   created = "CREATE" 
   updated = "UPDATE" 
   deleted = "DELETE" 
   
class ActionFlag(Enum):
   created = "NEW" 
   updated = "UPDATE" 
   deleted = "DELETE" 

class ErrorName(Enum):
   not_found = "not_found" 
   forbidden = "forbidden"
   unauthorized_access = "unauthorized_access"
   invalid_DiseaseType = "invalid_DiseaseType"
   invalid_DateFrom = "invalid_DateFrom"
   invalid_DateTo = "invalid_DateTo"
   invalid_NHSNumber = "invalid_NHSNumber"
   read_not_found = "read_not_found"
   doseNumberPositiveInt_PositiveInteger  = "doseNumberPositiveInt_PositiveInteger"
   doseNumberPositiveInt_ValidRange = "doseNumberPositiveInt_ValidRange"
   invalid_OccurrenceDateTime = "invalid_OccurrenceDateTime"
   invalid_recorded = "invalid_recorded"
   invalid_DateOfBirth = "invalid_DateOfBirth"
   invalid_expirationDate = "invalid_expirationDate"
   future_DateOfBirth = "future_DateOfBirth"
   
   
class SupplierNameWithODSCode(Enum):
   MAVIS= "V0V8L"
   SONAR= "8HK48"
   RAVS = "X8E5B" 
   PINNACLE = "8J1100001" 
   EMIS = "YGJ"
   TPP = "YGA" 
   MEDICUS = "YGMYW" 
   CEGEDIM = "YGM04"
   
class GenderCode(Enum):
    male = "1"
    female = "2"
    unknown = "0"
    other = "9"
