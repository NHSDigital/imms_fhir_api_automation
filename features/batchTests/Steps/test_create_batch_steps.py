from src.dynamoDB.dynamo_db_helper import *
from src.objectModels.api_immunization_builder import *
from src.objectModels.batch.batch_file_builder import *
from utilities.batch_S3_buckets import *
from utilities.batch_file_helper import *
from utilities.date_helper import *
from utilities.text_helper import get_text
from utilities.vaccination_constants import *
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from .batch_common_steps import *

scenarios('batchTests/create_batch.feature')

@given("batch file is created for below data")
@ignore_if_local_run
def valid_batch_file_is_created_with_details(datatable, context):    
    build_dataFrame_using_datatable(datatable, context)        
    create_batch_file(context)
    
@given("batch file is created for below data where date_and_time field has invalid date")
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_date_and_time(datatable, context):  
    build_dataFrame_using_datatable(datatable, context)   
    context.vaccine_df['DATE_AND_TIME'] = context.vaccine_df['UNIQUE_ID'].apply(lambda uid: get_batch_date(uid.split('-')[1]))     
    create_batch_file(context)   
    
@given("batch file is created for below data where recorded field has invalid date")
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_recorded_date(datatable, context):  
    build_dataFrame_using_datatable(datatable, context)   
    context.vaccine_df['RECORDED_DATE'] = context.vaccine_df['UNIQUE_ID'].apply(lambda uid: get_batch_date(uid.split('-')[1]))     
    create_batch_file(context)  
  
@given("batch file is created for below data where expiry field has invalid date")  
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_expiry_date(datatable, context):  
    build_dataFrame_using_datatable(datatable, context)   
    context.vaccine_df['EXPIRY_DATE'] = context.vaccine_df['UNIQUE_ID'].apply(lambda uid: get_batch_date(uid.split('-')[1]))     
    create_batch_file(context) 
    
@given("batch file is created for below data where Person date of birth field has invalid date")  
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_person_dateOfBirth_date(datatable, context):  
    build_dataFrame_using_datatable(datatable, context)   
    context.vaccine_df['PERSON_DOB'] = context.vaccine_df['UNIQUE_ID'].apply(lambda uid: get_batch_date(uid.split('-')[1]))     
    create_batch_file(context) 
    
@given("batch file is created for below data where Person detail has invalid data")
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_patient_data(datatable, context):
    build_dataFrame_using_datatable(datatable, context) 
    context.vaccine_df.loc[0,["NHS_NUMBER"]] = "12345678"
    context.vaccine_df.loc[1,["NHS_NUMBER"]] = "1234567890"
    context.vaccine_df.loc[2,["PERSON_FORENAME"]] = ""
    context.vaccine_df.loc[3,["PERSON_FORENAME", "PERSON_SURNAME"]] = ""
    context.vaccine_df.loc[4,["PERSON_SURNAME"]] = ""
    context.vaccine_df.loc[5,["PERSON_GENDER_CODE"]] = "8"
    context.vaccine_df.loc[6,["PERSON_GENDER_CODE"]] = "unknow"
    context.vaccine_df.loc[7,["PERSON_GENDER_CODE"]] = ""
    context.vaccine_df.loc[8,["PERSON_FORENAME"]] = " "
    context.vaccine_df.loc[9,["PERSON_SURNAME"]] = " "
    context.vaccine_df.loc[10,["PERSON_SURNAME"]] = get_text("name_length_36")
    context.vaccine_df.loc[11,["PERSON_FORENAME"]] = get_text("name_length_36")
    create_batch_file(context) 
    
@given("batch file is created for below data where performer detail has invalid data")
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_performer_data(datatable, context):
    build_dataFrame_using_datatable(datatable, context) 
    context.vaccine_df.loc[0,["PERFORMING_PROFESSIONAL_FORENAME"]] = ""
    context.vaccine_df.loc[1,["PERFORMING_PROFESSIONAL_SURNAME"]] = ""
    create_batch_file(context) 
    
@given("batch file is created for below data where person detail has valid values")
@ignore_if_local_run
def valid_batch_file_is_created_with_different_values_gender(datatable, context):
    build_dataFrame_using_datatable(datatable, context) 
    context.vaccine_df.loc[0,["PERSON_GENDER_CODE"]] = "0"
    context.vaccine_df.loc[1,["PERSON_GENDER_CODE"]] = "1"
    context.vaccine_df.loc[2,["PERSON_GENDER_CODE"]] = "2"
    context.vaccine_df.loc[3,["PERSON_GENDER_CODE"]] = "9"
    context.vaccine_df.loc[4,["PERSON_GENDER_CODE"]] = "unknown"
    context.vaccine_df.loc[5,["PERSON_GENDER_CODE"]] = "male"
    context.vaccine_df.loc[6,["PERSON_GENDER_CODE"]] = "female"
    context.vaccine_df.loc[7,["PERSON_GENDER_CODE"]] = "other"
    context.vaccine_df.loc[8,["PERSON_SURNAME"]] = get_text("name_length_35")
    context.vaccine_df.loc[9,["PERSON_FORENAME"]] = f"{get_text("name_length_35")}"
    context.vaccine_df.loc[10,["PERSON_FORENAME"]] = f"Elan {get_text("name_length_15")}"
    create_batch_file(context)

@then("all records are rejected in the bus ack file and no imms id is generated")
def all_record_are_rejected_for_given_field_name(context):
    all_valid = validate_bus_ack_file_for_error(context)
    assert all_valid, "One or more records failed validation checks"
 