@Create_Feature @Delete_cleanUp
Feature: Create the immunization event for a patient

Scenario Outline:  Verify that the POST Create API for different vaccine types
    Given valid token is generated for the '<Supplier>'
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
Scenario: verify that procedure term is mapped to text field in imms delta table
    Given Valid json payload is created where vaccination procedure term has text field populated
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The procedure term is mapped to text field in imms delta table

@vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: verify that procedure term is mapped to first instance of procedure code in imms delta table
    Given Valid json payload is created where vaccination procedure  has multiple instance of procedure code
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The procedure term is mapped to correct instance of coding display text field in imms delta table

@vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: verify that procedure term is mapped to correct instance of procedure code in imms delta table
    Given Valid json payload is created where vaccination procedure term multiple instance of procedure code with different coding system
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The procedure term is mapped to correct coding system value and display text field in imms delta table

@vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: verify that procedure term is mapped to code display of procedure code in imms delta table
    Given Valid json payload is created where vaccination procedure term has one instance of procedure code with no text or value string field
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The procedure term is mapped to correct coding display text field in imms delta table

