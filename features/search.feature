@Search_Feature
Feature: Search the immunization of a patient


# #   # Scenario: Verify that the Search will be successful with below valid parameters
# #   #   Given After passing all the valid parameters
# #   #     | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo |
# #   #     | 9449310610 | COVID19, FLU, RSV | Immunization:patient | None  | None  |    
# #   #   When Send a search request with GET method
# #   #   Then The search will be successful with the status code 200    


# #   # Scenario: Verify that the Search will throw error for an invalid patient NHS Number
# #   #   Given After passing all the valid parameters except an invalid nhsnumber
# #   #     | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo |
# #   #     | 944931060 | COVID19, FLU, RSV | Immunization:patient | None     | None   |
# #   #   When Send a search request with GET method
# #   #   Then The search will throw error with the status code 400    


#   Scenario Outline: Verify that the GET method of Search API will throw error for invalid format of patient identifier
#     Given With invalid format of the patient identifier "<PatientIdentifier>" and valid "<NHSNumber>", "<DiseaseType>", "<Include>", "<DateFrom>" & "<DateTo>" parameters
#     When Send a search request with GET method
#     Then The search will throw error with the status code 400
#     And The Search Response JSONs should contain the valid error message for invalid format of patient identifier

#     Examples: GETInvalidFormatPatientIdentifier
#       | PatientIdentifier  | NHSNumber  |   DiseaseType       | Include              | DateFrom | DateTo | Description                 |
#       | https://fhir.nhsssddfsd |  9449304424     | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Invalid Format of Patient Identifier  |
#       | https://nhs.uk/Id/nhs-number | 9449304424 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Invalid Format of Patient Identifier  |


#   Scenario Outline: Verify that the POST method of Search API will throw error for invalid format of patient identifier
#     Given With invalid format of the patient identifier "<PatientIdentifier>" and valid "<NHSNumber>", "<DiseaseType>", "<Include>", "<DateFrom>" & "<DateTo>" parameters
#     When Send a search request with POST method
#     Then The search will throw error with the status code 400
#     And The Search Response JSONs should contain the valid error message for invalid format of patient identifier

#     Examples: POSTInvalidFormatPatientIdentifier
#       | PatientIdentifier  | NHSNumber  |   DiseaseType       | Include              | DateFrom | DateTo | Description                 |
#       | https://fhir.nhsssddfsd |  9449304424     | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Invalid Format of Patient Identifier  |
#       | https://nhs.uk/Id/nhs-number | 9449304424 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Invalid Format of Patient Identifier  |      


#   Scenario Outline: Verify that the GET method of Search API will throw error for any mandatory query parameter having null value
#     Given With any of the mandatory parameters "<NHSNumber>" or "<DiseaseType>" are null and "<Include>", "<DateFrom>" & "<DateTo>" parameters havning valid value
#     When Send a search request with GET method
#     Then The search will throw error with the status code 400
#     And The Search Response JSONs should contain the valid error message for mandatory query parameters

#     Examples: GETNullMandatoryParameter
#       | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo | Description                 |
#       | null | COVID19, FLU, RSV | Immunization:patient | None     | None   | # NULL NHS Number  |
#       | 1234567890 | null | Immunization:patient | None     | None   | # NULL Disease Type  |


#   Scenario Outline: Verify that the POST method of Search API will throw error for any mandatory query parameter having null value
#     Given With any of the mandatory parameters "<NHSNumber>" or "<DiseaseType>" are null and "<Include>", "<DateFrom>" & "<DateTo>" parameters havning valid value
#     When Send a search request with POST method
#     Then The search will throw error with the status code 400
#     And The Search Response JSONs should contain the valid error message for mandatory query parameters

#     Examples: POSTNullMandatoryParameter
#       | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo | Description                 |
#       | null | COVID19, FLU, RSV | Immunization:patient | None     | None   | # NULL NHS Number  |
#       | 1234567890 | null | Immunization:patient | None     | None   | # NULL Disease Type  |      


#   Scenario Outline: Verify that the GET method of Search API will throw error for an invalid patient NHS Number
#     Given With the invalid "<NHSNumber>" and valid "<DiseaseType>", "<Include>", "<DateFrom>" & "<DateTo>" parameters
#     When Send a search request with GET method
#     Then The search will throw error with the status code 400
#     And The Search Response JSONs should contain the error message for invalid NHS Number

#     Examples: GETSearchInvalidNHSNumber
#       | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo | Description                       |
#       | 1234567890 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Invalid MOD11 check NHS Number  |
#       | 1 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Single Digit NHS Number  |
#       | 1000000000000000001 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Long NHS Number  |

@vaccine_type_RSV
Scenario Outline: Verify that the POST method of Search API will throw error for an invalid patient NHS Number
    When Send a search request with POST method With the invalid '<NHSNumber>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain the error message for invalid NHS Number

    Examples:
      | NHSNumber  |
      | 1234567890 | 
      | 1 |
      | 1000000000000000001 |    


#   ################## Scenario Outline: Verify that the GET method of Search API will throw error for an invalid Disease Type
#   ##################   Given With the invalid "<DiseaseType>" and valid "<NHSNumber>", "<Include>", "<DateFrom>" & "<DateTo>" parameters
#   ##################   When Send a search request with GET method
#   ##################   Then The search will throw error with the status code 400
#   ##################   And The Search Response JSONs should contain the error message for invalid Disease Type
# #################
#   ##################   Examples: GETSearchInvalidNHSNumber
#   ##################     | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo | Description                       |
#   ##################     | 9449304424 | COVID199, FLU, RSV | Immunization:patient | None     | None   | # Invalid MOD11 check NHS Number  |


#   Scenario Outline: Verify that the GET method of Search API will be successful with all the valid parameters
#     Given With the valid "<NHSNumber>", "<DiseaseType>", "<Include>", "<DateFrom>" & "<DateTo>" parameters
#     And Create an immunization event for the patient with the input JSONs available
#     When Send a search request with GET method for each Immunization event created
#     Then The search will be successful with the status code 200 for each Immunization event
#     And The Search Response JSONs should contain the detail of the immunization events created above
#     And The Search Response JSONs field values should match with the input JSONs field values for resourceType Immunization
#     And The Search Response JSONs field values should match with the input JSONs field values for resourceType Patient


#     Examples: GETSearchValidNHSNumber
#       | NHSNumber  | DiseaseType       | Include              | DateFrom | DateTo | Description                       |
#       | 9449304424 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Valid NHS Number                |
#     #   | 9452372249 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Supersede NHS Number            |
#       # | 9449310599 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Invalid in PDS NHS Number       |
#       # | 9452372230 | COVID19, FLU, RSV | Immunization:patient | None     | None   | # Old NHS Number                  |

@vaccine_type_RSV @patient_id_ValidNhs
Scenario: Verify that the POST method of Search API will be successful with all the valid parameters
    Given I have created a valid vaccination record
    When Send a search request with POST method for Immunization event create
    Then The request will be successful with the status code '200'
    And The Search Response JSONs should contain the detail of the immunization events created above
    And The Search Response JSONs field values should match with the input JSONs field values for resourceType Immunization
    And The Search Response JSONs field values should match with the input JSONs field values for resourceType Patient