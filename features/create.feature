@Create_Feature
Feature: Create the immunization event for a patient

Scenario Outline:  Verify that the POST Create API for different vaccine types
    Given Valid json payload is created with Patient '<Patient>' and vaccine_type '<vaccine_type>'
    When Trigger the post create request
    Then The request will be successful with the status code '201'
    And The location key in header will contain the Immunization Id
    And The X-Request-ID and X-Correlation-ID keys in header will populate correctly
    And The imms event table will be populated with the correct data for the above fields
    #And The delta table will be populated with the correct data for the above date fieldsbash

    Examples: 
      | Patient  | vaccine_type|
      |Random    | RSV         |
      |Random    | FLU         |

