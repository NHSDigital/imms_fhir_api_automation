Feature: Search the immunization of a patient

  # Scenario: Verify that the Search will be successful with a valid patient NHS Number
  #   Given After passing all the valid parameters
  #   When Send a search request with GET method
  #   Then The search will be successful with the status code 200

  Scenario: Verify that the Search will be successful with below valid parameters
    Given After passing all the valid parameters
      | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo |
      | 9449310610 | COVID19, FLU, RSV | Immunization:patient | None  | None  |    
    When Send a search request with GET method
    Then The search will be successful with the status code 200    

  Scenario: Verify that the Search will throw error for an invalid patient NHS Number
    Given After passing all the valid parameters except an invalid nhsnumber
      | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo |
      | 944931060 | COVID19, FLU, RSV | Immunization:patient | None     | None   |
    When Send a search request with GET method
    Then The search will be throw error with the status code 400    

  Scenario Outline: Verify that the Search will throw error for an invalid patient NHS Number
    Given Pass the invalid "<NHSNumber>" and valid "<DiseaseType>", "<Include>", "<DateFrom>" & "<DateTo>" parameters
    When Send a search request with GET method
    Then The search will be throw error with the status code 400

    Examples: InvalidNHSNumber
      | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo |
      | 9449310610 | COVID19, FLU, RSV | Immunization:patient | None     | None   |
