@Create_Feature @Delete_cleanUp
Feature: Create the immunization event for a patient

Scenario Outline:  Verify that the POST Create API for different vaccine types
    Given Valid token is generated for the '<Supplier>'
    And Valid json payload is created with Patient '<Patient>' and vaccine_type '<vaccine_type>'
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The X-Request-ID and X-Correlation-ID keys in header will populate correctly
    And The imms event table will be populated with the correct data for 'created' event
    And The delta table will be populated with the correct data for created event

    Examples: 
      | Patient  | vaccine_type| Supplier     |
      |Random    | COVID19     | RAVS         |
      |Random    | RSV         | Postman_Auth |
      |Random    | FLU         | MAVIS        |

@vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM fields are mapped to respective text fields in imms delta table
    Given Valid json payload is created where vaccination terms has text field populated
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The terms are mapped to the respective text fields in imms delta table

@vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM fields are mapped to first instance of coding.display fields in imms delta table
    Given Valid json payload is created where vaccination terms has multiple instances of coding
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The terms are mapped to first instance of coding.display fields in imms delta table

@vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM fields are mapped to correct instance of coding.display fields in imms delta table
    Given Valid json payload is created where vaccination terms has multiple instance of coding with different coding system
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The terms are mapped to correct instance of coding.display fields in imms delta table

@vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM fields are mapped to coding.display in imms delta table in case of only one instance of coding
    Given Valid json payload is created where vaccination terms has one instance of coding with no text or value string field
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The terms are mapped to correct coding.display fields in imms delta table

@vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that VACCINATION_PROCEDURE_TERM, VACCINE_PRODUCT_TERM, SITE_OF_VACCINATION_TERM, ROUTE_OF_VACCINATION_TERM fields are blank in imms delta table if no text or value string or display field is present
    Given Valid json payload is created where vaccination terms has no text or value string or display field
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The terms are blank in imms delta table    

