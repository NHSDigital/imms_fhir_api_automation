ERROR_MAP = {
    "Common_field": {
        "resourceType": "OperationOutcome",
        "profile": "https://simplifier.net/guide/UKCoreDevelopment2/ProfileUKCore-OperationOutcome",
        "system": "https://fhir.nhs.uk/Codesystem/http-error-codes",
        "severity": "error",
    },
    "invalid_DateFrom_Include": {        
        "code": "INVALID",
        "diagnostics": "Search parameter -date.from must be in format: YYYY-MM-DD; Search parameter _include may only be 'Immunization:patient' if provided."
    },
    "invalid_NHSNumber": {        
        "code": "INVALID",
        "diagnostics": "Search parameter patient.identifier must be a valid NHS number."
    },
    "invalid_include": {        
        "code": "INVALID",
        "diagnostics": "Search parameter _include may only be 'Immunization:patient' if provided."
    },
    "invalid_DateFrom_To": {        
        "code": "INVALID",
        "diagnostics": "Search parameter -date.from must be in format: YYYY-MM-DD; Search parameter -date.to must be in format: YYYY-MM-DD"
    },
    "invalid_DateFrom_DateTo_Include": {        
        "code": "INVALID",
        "diagnostics": "Search parameter -date.from must be in format: YYYY-MM-DD; Search parameter -date.to must be in format: YYYY-MM-DD; Search parameter _include may only be 'Immunization:patient' if provided."
    },
    "invalid_DiseaseType": {
        "code": "INVALID",
        "diagnostics": "immunization-target must be one or more of the following: RSV, COVID19, MMR, MENACWY, FLU, HPV, 3IN1"
    },
    "invalid_DateFrom": {
        "code": "INVALID",
        "diagnostics": "Search parameter -date.from must be in format: YYYY-MM-DD"
    }, 
    "invalid_DateTo": {
        "code": "INVALID",
        "diagnostics": "Search parameter -date.to must be in format: YYYY-MM-DD"
    },  
    "unauthorized_access": {
        "code": "FORBIDDEN",
        "diagnostics": "Unauthorized request for vaccine type"
    },  
    "not_found": {
        "code": "NOT-FOUND",
        "diagnostics": f"Immunization resource does not exist."
    },      
    "forbidden": {
        "code": "FORBIDDEN",
        "diagnostics": f"Unauthorized request for vaccine type"
    },
    "doseNumberPositiveInt_PositiveInteger": {
        "code": "INVARIANT",
        "diagnostics": "Validation errors: protocolApplied[0].doseNumberPositiveInt must be a positive integer"
    },
    "doseNumberPositiveInt_ValidRange": {
        "code": "INVARIANT",
        "diagnostics": "Validation errors: protocolApplied[0].doseNumberPositiveInt must be an integer in the range 1 to 9"
    },
    "invalid_OccurrenceDateTime": {
        "code": "INVARIANT",
        "diagnostics": "Validation errors: occurrenceDateTime must be a valid datetime in one of the following formats:- 'YYYY-MM-DD' — Full date only- 'YYYY-MM-DDThh:mm:ss%z' — Full date and time with timezone (e.g. +00:00 or +01:00)- 'YYYY-MM-DDThh:mm:ss.f%z' — Full date and time with milliseconds and timezone- Date must not be in the future.Only '+00:00' and '+01:00' are accepted as valid timezone offsets.Note that partial dates are not allowed for occurrenceDateTime in this service."
    },
    "invalid_recorded": {
        "code": "INVARIANT",
        "diagnostics": "Validation errors: recorded must be a valid datetime in one of the following formats:- 'YYYY-MM-DD' — Full date only- 'YYYY-MM-DDThh:mm:ss%z' — Full date and time with timezone (e.g. +00:00 or +01:00)- 'YYYY-MM-DDThh:mm:ss.f%z' — Full date and time with milliseconds and timezone- Date must not be in the future."
    },
    "future_DateOfBirth": {
        "code": "INVARIANT",
        "diagnostics": "Validation errors: contained[?(@.resourceType=='Patient')].birthDate must not be in the future"
    },
    "invalid_DateOfBirth": {
        "code": "INVARIANT",
        "diagnostics": "Validation errors: contained[?(@.resourceType=='Patient')].birthDate must be a valid date string in the format \"YYYY-MM-DD\""
    },
    "invalid_expirationDate": {
        "code": "INVARIANT",
        "diagnostics": 'Validation errors: expirationDate must be a valid date string in the format \"YYYY-MM-DD\"'
    }  
}

