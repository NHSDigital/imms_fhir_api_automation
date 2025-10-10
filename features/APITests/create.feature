@Create_Feature 
Feature: Create the immunization event for a patient

@Delete_cleanUp
Scenario Outline:  Verify that the POST Create API for different vaccine types
    Given Valid token is generated for the '<Supplier>'
    And Valid json payload is created with Patient '<Patient>' and vaccine_type '<vaccine_type>'
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key and Etag in header will contain the Immunization Id and version
    And The X-Request-ID and X-Correlation-ID keys in header will populate correctly
    And The imms event table will be populated with the correct data for 'created' event
    And The delta table will be populated with the correct data for created event

    Examples: 
      | Patient  | vaccine_type| Supplier     |
      |Random    | COVID19     | Postman_Auth |
      |Random    | RSV         | RAVS         |
      |Random    | FLU         | MAVIS        |
      |Random    | MMR         | Postman_Auth |
      |Random    | MENACWY     | MAVIS        |
      |Random    | 3in1        | MAVIS        |

@Delete_cleanUp @vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM fields are mapped to respective text fields in imms delta table
    Given Valid json payload is created where vaccination terms has text field populated
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key and Etag in header will contain the Immunization Id and version
    And The terms are mapped to the respective text fields in imms delta table

@Delete_cleanUp @vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM fields are mapped to first instance of coding.display fields in imms delta table
    Given Valid json payload is created where vaccination terms has multiple instances of coding
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key and Etag in header will contain the Immunization Id and version
    And The terms are mapped to first instance of coding.display fields in imms delta table

@Delete_cleanUp @vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM fields are mapped to correct instance of coding.display fields in imms delta table
    Given Valid json payload is created where vaccination terms has multiple instance of coding with different coding system
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key and Etag in header will contain the Immunization Id and version
    And The terms are mapped to correct instance of coding.display fields in imms delta table

@Delete_cleanUp @vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM fields are mapped to coding.display in imms delta table in case of only one instance of coding
    Given Valid json payload is created where vaccination terms has one instance of coding with no text or value string field
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key and Etag in header will contain the Immunization Id and version
    And The terms are mapped to correct coding.display fields in imms delta table

@Delete_cleanUp @vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM fields are blank in imms delta table if no text or value string or display field is present
    Given Valid json payload is created where vaccination terms has no text or value string or display field
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key and Etag in header will contain the Immunization Id and version
    And The terms are blank in imms delta table 

Scenario Outline:  Verify that the POST Create API for different supplier fails on access denied
    Given Valid token is generated for the '<Supplier>'
    And Valid json payload is created with Patient '<Patient>' and vaccine_type '<vaccine_type>'
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '403'
    And The Response JSONs should contain correct error message for 'unauthorized_access' access
    Examples: 
      | Patient  | vaccine_type| Supplier     |
      |Random    | HPV         |  RAVS        |
      |Random    | RSV         | MAVIS        |
      |Random    | RSV         | SONAR        |

@Delete_cleanUp @supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Mod11_NHS
Scenario:  Verify that the POST Create API for invalid but Mod11 compliant NHS Number 
    Given Valid json payload is created
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key and Etag in header will contain the Immunization Id and version
    And The X-Request-ID and X-Correlation-ID keys in header will populate correctly
    And The imms event table will be populated with the correct data for 'created' event
    And The delta table will be populated with the correct data for created event

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario Outline:  Verify that the POST Create API will fail if doseNumberPositiveInt is not valid
    Given Valid json payload is created where doseNumberPositiveInt is '<doseNumberPositiveInt>'
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for '<error_type>'
    Examples: 
      | doseNumberPositiveInt | error_type                                  |
      | -1                    | doseNumberPositiveInt_PositiveInteger       |
      | 0                     | doseNumberPositiveInt_PositiveInteger       |
      | 10                    | doseNumberPositiveInt_ValidRange            |


@Delete_cleanUp @supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario: Verify that the POST Create API will be successful if all date field has valid past date
    Given Valid json payload is created where date fields has past date
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key and Etag in header will contain the Immunization Id and version


@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario Outline: Verify that the POST Create API will fail if occurrenceDateTime has future or invalid formatted date
    Given Valid json payload is created where occurrenceDateTime has invalid '<Date>' date
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'invalid_OccurrenceDateTime'
     Examples: 
        | Date                  | 
        | future_occurrence     | 
        | invalid_format        |
        | nonexistent           |
        | empty                 |

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario Outline: Verify that the POST Create API will fail if recorded has future or invalid formatted date
    Given Valid json payload is created where recorded has invalid '<Date>' date
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'invalid_recorded'
     Examples: 
        | Date                  | 
        | future_date           | 
        | invalid_format        |
        | nonexistent           |
        | empty                 |

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario Outline: Verify that the POST Create API will fail if patient's data of birth has future or invalid formatted date
    Given Valid json payload is created where date of birth has invalid '<Date>' date
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for '<error_type>'
     Examples: 
        | Date                  | error_type            |   
        | future_date           | future_DateOfBirth    |
        | invalid_format        | invalid_DateOfBirth   |
        | nonexistent           | invalid_DateOfBirth   |
        | empty                 | invalid_DateOfBirth   |

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario Outline: Verify that the POST Create API will fail if expiration date has invalid formatted date
    Given Valid json payload is created where expiration date has invalid '<Date>' date
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'invalid_expirationDate'
     Examples: 
        | Date                  | 
        | invalid_format        |
        | nonexistent           |
        | empty                 |

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario Outline: Verify that the POST Create API will fail if nhs number is invalid
    Given Valid json payload is created where Nhs number is invalid '<invalid_NhsNumber>' 
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for '<error_type>'
    Examples: 
    |invalid_NhsNumber  |error_type                 |
    |1234567890         |invalid_Mod11_NhsNumber    |
    |12345678           |invalid_NHSNumber_length   |

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario: Verify that the POST Create API will fail if patient forename is empty
    Given Valid json payload is created where patient forename is empty
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'empty_forename'

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario: Verify that the POST Create API will fail if patient forename array is not present
    Given Valid json payload is created where patient forename is not array
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'no_forename'

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario: Verify that the POST Create API will fail if patient Surname is empty
    Given Valid json payload is created where patient surname is empty
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'empty_surname'

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario: Verify that the POST Create API will fail if patient name is empty
    Given Valid json payload is created where patient name is empty
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'empty_forename_surname'

@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario: Verify that the POST Create API will fail if patient gender is invalid
    Given Valid json payload is created where patient gender is invalid
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'invalid_gender'
    
@supplier_name_Postman_Auth @vaccine_type_RSV @patient_id_Random
Scenario: Verify that the POST Create API will fail if patient gender is empty
    Given Valid json payload is created where patient gender is empty
    When Trigger the post create request
    Then The request will be unsuccessful with the status code '400'
    And The Response JSONs should contain correct error message for 'empty_gender'  