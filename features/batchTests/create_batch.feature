@Create_Batch_Feature
Feature: Create the immunization event for a patient through batch file


@delete_cleanup_batch @vaccine_type_HPV  @supplier_name_MAVIS
Scenario: Verify that vaccination record will be created for different vaccine types through batch file
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
  
