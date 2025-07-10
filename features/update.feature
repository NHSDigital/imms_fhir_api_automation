@Update_Feature
Feature: Update the immunization of a patient

@Delete_cleanUp @vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that the Delete API will be successful with all the valid parameters
    Given I have created a valid vaccination record
    When Send a update for Immunization event created with patient address being updated
    Then The request will be successful with the status code '200'
    And The X-Request-ID and X-Correlation-ID keys in header will populate correctly
    And The imms event table will be populated with the correct data for 'updated' event
    And The delta table will be populated with the correct data for updated event


@vaccine_type_RSV @patient_id_Random
Scenario: Verify that the updated event request will fail with forbidden access for MAVIS supplier
    Given valid vaccination record is created by 'RAVS' supplier 
    When Send a update for Immunization event created with patient address being updated by 'MAVIS'
    Then The request will be successful with the status code '403'
    And The Response JSONs should contain correct error message for forbidden access