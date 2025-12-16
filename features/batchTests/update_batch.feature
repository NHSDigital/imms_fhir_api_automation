@Update_Batch_Feature @functional
Feature: Create the immunization event for a patient through batch file and update the record from batch or Api calls

@delete_cleanup_batch @vaccine_type_MMR  @supplier_name_TPP
Scenario: Update immunization event for a patient through batch file
    Given batch file is created for below data as full dataset and each record has a valid update record in te same file 
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
    And bus ack will not have any entry of successfully processed records
    And Audit table will have correct status, queue name and record count for the processed batch file
    And The imms event table will be populated with the correct data for 'updated' event for records in batch file
    And The delta table will be populated with the correct data for all created records in batch file 
    And The delta table will be populated with the correct data for all updated records in batch file 