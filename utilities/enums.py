from enum import Enum

class Operation(Enum):
   created = "CREATE" 
   updated = "UPDATE" 
   deleted = "DELETE" 
   
class ActionFlag(Enum):
   created = "NEW" 
   updated = "UPDATE" 
   deleted = "DELETE" 
   
class SupplierNameWithODSCode(Enum):
   MAVIS= "V0V8L"
   SONAR= "8HK48"
   RAVS = "X8E5B" 
   PINNACLE = "8J1100001" 
   OPTUM = "YGJ"
   TPP = "YGA" 
   MEDICUS = "YGMYW" 
   CEGEDIM = "YGM04"
   Postman_Auth = "Postman_Auth"
   
class GenderCode(Enum):
    male = "1"
    female = "2"
    unknown = "0"
    other = "9"
