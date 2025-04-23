@Create_Feature
Feature: Create the immunization event for a patient

  Scenario Outline: Verify that the POST Create API will create an Immunization event and populate the imms event and delta dynamodb tables correctly
    Given Prepare create paylod with "<NHSNumber>", "<birthDate>", "<occurrenceDateTime>", "<recorded>", "<expirationDate>"
    When Send a create request with POST method for the input JSONs available 
    Then The create will be successful with the status code 201
    And The location key in header will contain the Immunization Id
    And The X-Request-ID and X-Correlation-ID keys in header will populate correctly
    And The imms event table will be populated with the correct data for the above fields
    # And The delta table will be populated with the correct data for the above date fields

    Examples: POSTCreateDeltaDates
      | NHSNumber  | birthDate       | occurrenceDateTime              | recorded                           | expirationDate | Description                  |
      | 9452372249 | 1980-01-01      | 2025-03-06T13:28:17.271+00:00   | 2025-03-06T13:28:17.271+00:00      | 2025-07-02     | # Valid Values               |
