@Create_Batch_Feature
Feature: Create the immunization event for a patient through batch file


@Delete_cleanUp @vaccine_type_HPV  @supplier_name_MAVIS
Scenario: Verify that vaccination record will be created for different vaccine types through batch file
    Given batch file is created for below data
        | patient_id        | unique_id            |
        | Random            | Valid_NHsNumber      |
        | InvalidInPDS      | InvalidInPDS_NhsNUmber |
        | SFlag             | SFlag_NhsNumber       |
        | Mod11_NHS         | Mod11_NHSNumber       |
        | OldNHSNo          | OldNHSNo              |
    When batch file upload in s3 bucket
    Then file will be moved to destination bucket
    And all records are processed successfully in the batch file 
  
