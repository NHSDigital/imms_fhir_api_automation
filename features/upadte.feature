@Update_Feature
Feature: Update the immunization of a patient

@Delete_cleanUp @vaccine_type_RSV @patient_id_Random @supplier_name_RAVS
Scenario: Verify that the Delete API will be successful with all the valid parameters
    Given I have created a valid vaccination record
    When Send a update for Immunization event created with patient address being updated
    Then The request will be successful with the status code '204'
    And The X-Request-ID and X-Correlation-ID keys in header will populate correctly
    And The imms event table will be populated with the correct data for 'updated' event
    And The delta table will be populated with the correct data for updated event