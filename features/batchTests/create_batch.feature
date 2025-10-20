@Create_Batch_Feature
Feature: Create the immunization event for a patient through batch file

@delete_cleanup_batch @vaccine_type_HPV  @supplier_name_MAVIS
Scenario: Verify that vaccination record will be created through batch file
    Given batch file is created for below data
        | patient_id        | unique_id             |
        | Random            | Valid_NhsNumber       |
        | InvalidInPDS      | InvalidInPDS_NhsNumber|
        | SFlag             | SFlag_NhsNumber       |
        | Mod11_NHS         | Mod11_NhSNumber       |
        | OldNHSNo          | OldNHSNo              |
    When batch file is uploaded in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are processed successfully in the bus ack file 
    And Audit table will have correct status, queue name and record count for the processed batch file
    And The imms event table will be populated with the correct data for 'created' event for records in batch file
    And The delta table will be populated with the correct data for all records in batch file  

@vaccine_type_HPV  @supplier_name_MAVIS
Scenario: Verify that vaccination record will be get rejected if date_and_time is invalid in batch file
    Given batch file is created for below data where date_and_time field has invalid date 
        | patient_id        | unique_id                                                |
        | Random            | Fail-future_occurrence-invalid_OccurrenceDateTime        |
        | Random            | Fail-invalid_batch_occurrence-invalid_OccurrenceDateTime |
        | Random            | Fail-nonexistent-invalid_OccurrenceDateTime              |
        | Random            | Fail-empty-empty_OccurrenceDateTime                                  |
    When batch file is uploaded in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated
    And Audit table will have correct status, queue name and record count for the processed batch file

@vaccine_type_HPV  @supplier_name_MAVIS
Scenario: verify that vaccination record will be get rejected if recorded_date is invalid in batch file
    Given batch file is created for below data where recorded field has invalid date 
        | patient_id        | unique_id                            |
        | Random            | Fail-future_date-invalid_recorded    |
        | Random            | Fail-invalid_format-invalid_recorded |
        | Random            | Fail-nonexistent-invalid_recorded    |
        | Random            | Fail-empty-empty_recorded            |
    When batch file is uploaded in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated
    And Audit table will have correct status, queue name and record count for the processed batch file

@vaccine_type_HPV  @supplier_name_MAVIS
Scenario: verify that vaccination record will be get rejected if expiry_date is invalid in batch file
    Given batch file is created for below data where expiry field has invalid date 
        | patient_id        | unique_id                                  |
        | Random            | Fail-invalid_format-invalid_expirationDate |
        | Random            | Fail-nonexistent-invalid_expirationDate    |
    When batch file is uploaded in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated
    And Audit table will have correct status, queue name and record count for the processed batch file

@vaccine_type_HPV  @supplier_name_MAVIS
Scenario: verify that vaccination record will be get rejected if Person date of birth is invalid in batch file
    Given batch file is created for below data where Person date of birth field has invalid date 
        | patient_id        | unique_id                               |
        | Random            | Fail-future_date-future_DateOfBirth     |
        | Random            | Fail-invalid_format-invalid_DateOfBirth |
        | Random            | Fail-nonexistent-invalid_DateOfBirth    |
        | Random            | Fail-empty-missing_DateOfBirth          |
    When batch file is uploaded in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated 
    And Audit table will have correct status, queue name and record count for the processed batch file

@vaccine_type_HPV  @supplier_name_MAVIS
Scenario: verify that vaccination record will be get rejected if Person nhs number, name and gender is invalid in batch file
    Given batch file is created for below data where Person detail has invalid data
        | patient_id        | unique_id                                        |                               
        | Random            | Fail-invalid_NhsNumber-invalid_NHSNumber_length  |
        | Random            | Fail-not_MOD11_NhsNumber-invalid_Mod11_NhsNumber |
        | Random            | Fail-empty_patient_forename-no_forename          |
        | Random            | Fail-empty_patient_name-empty_forename_surname   |
        | Random            | Fail-empty_patient_surname-no_surname            |
        | Random            | Fail-invalid_gender_code-invalid_gender          |  
        | Random            | Fail-invalid_gender-invalid_gender               |  
        | Random            | Fail-empty_gender-missing_gender                 | 
        | Random            | Fail-white_space_forename-empty_array_item_forename            |
        | Random            | Fail-white_space_surname-empty_surname           | 
        | Random            | Fail-name_length_36-max_len_surname              | 
        | Random            | Fail-name_length_36-max_len_forename             | 
    When batch file is uploaded in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated
    And Audit table will have correct status, queue name and record count for the processed batch file 

@vaccine_type_HPV  @supplier_name_MAVIS
Scenario: verify that vaccination record will be get successful if performer is invalid in batch file
    Given batch file is created for below data where performer detail has invalid data
        | patient_id        | unique_id                |
        | Random            | empty_performer_forename |
        | Random            | empty_performer_Surname  |
    When batch file is uploaded in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are processed successfully in the bus ack file 
    And Audit table will have correct status, queue name and record count for the processed batch file
    And The imms event table will be populated with the correct data for 'created' event for records in batch file
    And The delta table will be populated with the correct data for all records in batch file  

@vaccine_type_FLU  @supplier_name_SONAR
Scenario: verify that vaccination record will be get successful with different valid value in gender field
    Given batch file is created for below data where person detail has valid values
        | patient_id        | unique_id                   |
        | Random            | gender_value_0              |
        | Random            | gender_value_1              |
        | Random            | gender_value_2              |
        | Random            | gender_value_9              |
        | Random            | gender_value_Not-Known      |
        | Random            | gender_value_male           |
        | Random            | gender_value_female         |
        | Random            | gender_value_not-Specified  |
        | Random            | patient_surname_max_length  |
        | Random            | patient_forename_max_length |
        | Random            | patient_forename_max_length_multiple_values |
    When batch file is uploaded in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are processed successfully in the bus ack file 
    And Audit table will have correct status, queue name and record count for the processed batch file
    And The imms event table will be populated with the correct data for 'created' event for records in batch file
    And The delta table will be populated with the correct data for all records in batch file 