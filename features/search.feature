@Search_Feature
Feature: Search the immunization of a patient

# Positive Scenarios
Scenario Outline: Verify that the GET method of Search API will be successful with all the valid parameters
    Given Valid vaccination record is created with Patient '<Patient>' and vaccine_type '<Vaccine_type>'
    When Send a search request with GET method for Immunization event created
    Then The request will be successful with the status code '200'
    And The Search Response JSONs should contain the detail of the immunization events created above
    And The Search Response JSONs field values should match with the input JSONs field values for resourceType Immunization
    And The Search Response JSONs field values should match with the input JSONs field values for resourceType Patient
    Examples: 
      |Patient       | Vaccine_type|
      |Random        | RSV         |
      |SFlag         | RSV         |
      |SupersedeNhsNo| RSV         |
      |Random        | FLU         |
      |SFlag         | FLU         |
      |SupersedeNhsNo| FLU         |
      |Random        | COVID19     |
      |SFlag         | COVID19     |
      |SupersedeNhsNo| COVID19     |


Scenario Outline: Verify that the POST method of Search API will be successful with all the valid parameters 
    Given Valid vaccination record is created with Patient '<Patient>' and vaccine_type '<Vaccine_type>'
    When Send a search request with POST method for Immunization event created
    Then The request will be successful with the status code '200'
    And The Search Response JSONs should contain the detail of the immunization events created above
    And The Search Response JSONs field values should match with the input JSONs field values for resourceType Immunization
    And The Search Response JSONs field values should match with the input JSONs field values for resourceType Patient
    Examples: 
      |Patient       | Vaccine_type|
      |Random        | RSV         |
      |SFlag         | RSV         |
      |SupersedeNhsNo| RSV         |
      |Random        | FLU         |
      |SFlag         | FLU         |
      |SupersedeNhsNo| FLU         |
      |Random        | COVID19     |
      |SFlag         | COVID19     |
      |SupersedeNhsNo| COVID19     | 


Scenario Outline: Verify that the immunisation events retrieved in the response of Search API should be within Date From and Date To range
    When Send a search request with GET method with valid NHS Number '<NHSNumber>' and Disease Type '<vaccine_type>' and Date From '<DateFrom>' and Date To '<DateTo>'
    Then The request will be successful with the status code '200'
    And The occurrenceDateTime of the immunization events should be within the Date From and Date To range
    When Send a search request with POST method with valid NHS Number '<NHSNumber>' and Disease Type '<vaccine_type>' and Date From '<DateFrom>' and Date To '<DateTo>'
    Then The request will be successful with the status code '200'
    And The occurrenceDateTime of the immunization events should be within the Date From and Date To range

    Examples: 
      |NHSNumber        | vaccine_type | DateFrom   |  DateTo    |
      |9728403348       | COVID19      | 2025-06-18 | 2025-06-25 |

# Negative Scenarios

Scenario Outline: Verify that Search API will throw error if NHS Number is invalid
    When Send a search request with GET method with invalid NHS Number '<NHSNumber>' and valid Disease Type '<DiseaseType>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid NHS Number
    When Send a search request with POST method with invalid NHS Number '<NHSNumber>' and valid Disease Type '<DiseaseType>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid NHS Number

    Examples:
      | NHSNumber  |        DiseaseType       |
      |   ""       |        COVID19           |
      | 1234567890 |        RSV               |
      | 1          |        COVID19           |
      | 10000000000 00001 | COVID19           |


Scenario Outline: Verify that Search API will throw error if Disease Type is invalid
    When Send a search request with GET method with valid NHS Number '<NHSNumber>' and invalid Disease Type '<DiseaseType>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Disease Type
    When Send a search request with POST method with valid NHS Number '<NHSNumber>' and invalid Disease Type '<DiseaseType>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Disease Type

    Examples:
      | NHSNumber  |        DiseaseType       |
      | 9449304424 |        ""                |
      | 9449304424 |        FLu               |
      | 9449304424 |        ABC               |   


Scenario Outline: Verify that Search API will throw error if both NHS Number and Disease Type are invalid
    When Send a search request with GET method with invalid NHS Number '<NHSNumber>' and invalid Disease Type '<DiseaseType>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Disease Type
    When Send a search request with POST method with invalid NHS Number '<NHSNumber>' and invalid Disease Type '<DiseaseType>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Disease Type

    Examples:
      | NHSNumber  |        DiseaseType       |
      | 1234567890 |        ABC               |
      |   ""       |        ""                |


Scenario Outline: Verify that Search API will throw error if date from is invalid
    When Send a search request with GET method with invalid Date From '<DateFrom>' and valid Date To '<DateTo>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Date From
    When Send a search request with POST method with invalid Date From '<DateFrom>' and valid Date To '<DateTo>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Date From    

    Examples:
      | DateFrom      |        DateTo       |
      | 999-06-01     |        2025-06-01   |
      | 2025-13-01    |        2025-06-01   |    
      | 2025-05-32    |        2025-06-01   |    


Scenario Outline: Verify that Search API will throw error if date to is invalid
    When Send a search request with GET method with valid Date From '<DateFrom>' and invalid Date To '<DateTo>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Date To
    When Send a search request with POST method with valid Date From '<DateFrom>' and invalid Date To '<DateTo>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Date To    

    Examples:
      | DateFrom      |        DateTo       |
      | 2025-05-01    |        999-06-01    |
      | 2025-05-01    |        2025-13-01   |    
      | 2025-05-01    |        2025-05-32   |  


Scenario Outline: Verify that Search API will throw error if both date from and date to are invalid
    When Send a search request with GET method with invalid Date From '<DateFrom>' and invalid Date To '<DateTo>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Date From
    When Send a search request with POST method with invalid Date From '<DateFrom>' and invalid Date To '<DateTo>'
    Then The request will be unsuccessful with the status code '400'
    And The Search Response JSONs should contain correct error message for invalid Date From    

    Examples:
      | DateFrom      |        DateTo       |
      | 999-06-01     |        999-06-01    |
      | 2025-13-01    |        2025-13-01   |    
      | 2025-05-32    |        2025-05-32   |  

