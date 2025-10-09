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
    When batch file upload in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are processed successfully in the bus ack file 
    And Audit table will have correct status and queue name for the processed batch file
    And The imms event table will be populated with the correct data for 'created' event for records in batch file
    And The delta table will be populated with the correct data for all records in batch file
  

@vaccine_type_HPV  @supplier_name_MAVIS
Scenario: Verify that vaccination record will be get rejected if date_and_time is invalid in batch file
    Given batch file is created for below data where date_and_time field has invalid date 
        | patient_id        | unique_id                                          |
        | Random            | Fail-future_occurrence-invalid_OccurrenceDateTime  |
        | Random            | Fail-current_occurrence-invalid_OccurrenceDateTime |
        | Random            | Fail-nonexistent-invalid_OccurrenceDateTime        |
        | Random            | Fail-empty-empty_string                            |
    When batch file upload in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated

@vaccine_type_hpv  @supplier_name_MAVIS
Scenario: verify that vaccination record will be get rejected if recorded_date is invalid in batch file
    Given batch file is created for below data where recorded field has invalid date 
        | patient_id        | unique_id                            |
        | Random            | Fail-future_date-invalid_recorded    |
        | Random            | Fail-invalid_format-invalid_recorded |
        | Random            | Fail-nonexistent-invalid_recorded    |
        | Random            | Fail-empty-empty_string              |
    When batch file upload in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated

@vaccine_type_hpv  @supplier_name_MAVIS
Scenario: verify that vaccination record will be get rejected if expiry_date is invalid in batch file
    Given batch file is created for below data where expiry field has invalid date 
        | patient_id        | unique_id                                  |
        | Random            | Fail-invalid_format-invalid_expirationDate |
        | Random            | Fail-nonexistent-invalid_expirationDate    |
        | Random            | Fail-empty-invalid_expirationDate          |
    When batch file upload in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated

@vaccine_type_hpv  @supplier_name_MAVIS
Scenario: verify that vaccination record will be get rejected if Person date of birth is invalid in batch file
    Given batch file is created for below data where Person date of birth field has invalid date 
        | patient_id        | unique_id                               |
        | Random            | Fail-future_date-future_DateOfBirth     |
        | Random            | Fail-invalid_format-invalid_DateOfBirth |
        | Random            | Fail-nonexistent-invalid_DateOfBirth    |
        | Random            | Fail-empty-empty_string                 |
    When batch file upload in s3 bucket
    Then file will be moved to destination bucket and inf ack file will be created
    And inf ack file has success status for processed batch file
    And bus ack file will be created
    And all records are rejected in the bus ack file and no imms id is generated 