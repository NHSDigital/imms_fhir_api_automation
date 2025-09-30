@Create_Batch_Feature
Feature: Create the immunization event for a patient through batch file


@Delete_cleanUp @vaccine_type_HPV @patient_id_Random @supplier_name_MAVIS
Scenario Outline:  Verify that vaccination record will be created for different vaccine types through batch file
    Given Valid batch file is created 
    When batch file upload in s3 bucket
  
