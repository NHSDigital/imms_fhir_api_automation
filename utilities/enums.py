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
   