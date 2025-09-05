@Read_Feature
Feature: Read the immunization of a patient

@Delete_cleanUp @supplier_name_Postman_Auth
Scenario Outline: Verify that the Read method of API will be successful and fetch valid imms event detail 
    Given Valid vaccination record is created with Patient '<Patient>' and vaccine_type '<Vaccine_type>'
    When Send a read request for Immunization event created
    Then The request will be successful with the status code '200'
    And The Etag in header will containing the latest event version
    And The X-Request-ID and X-Correlation-ID keys in header will populate correctly
    And The Read Response JSONs field values should match with the input JSONs field values

    Examples: 
      |Patient       | Vaccine_type|
      |Random        | RSV         |
      |Random        | FLU         |
      |Random        | COVID19     |

