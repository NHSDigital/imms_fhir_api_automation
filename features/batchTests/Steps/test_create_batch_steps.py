from src.dynamoDB.dynamo_db_helper import *
from src.objectModels.api_immunization_builder import *
from src.objectModels.batch.batch_file_builder import *
from utilities.batch_S3_buckets import *
from utilities.batch_file_helper import *
from utilities.date_helper import *
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
    context.vaccine_df['DATE_AND_TIME'] = context.vaccine_df['UNIQUE_ID'].apply(lambda uid: get_date(uid.split('-')[1]))     
    create_batch_file(context)   
    
@given("batch file is created for below data where recorded field has invalid date")
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_recorded_date(datatable, context):  
    build_dataFrame_using_datatable(datatable, context)   
    context.vaccine_df['RECORDED_DATE'] = context.vaccine_df['UNIQUE_ID'].apply(lambda uid: get_date(uid.split('-')[1]))     
    create_batch_file(context)  
  
@given("batch file is created for below data where expiry field has invalid date")  
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_expiry_date(datatable, context):  
    build_dataFrame_using_datatable(datatable, context)   
    context.vaccine_df['EXPIRY_DATE'] = context.vaccine_df['UNIQUE_ID'].apply(lambda uid: get_date(uid.split('-')[1]))     
    create_batch_file(context) 
    
@given("batch file is created for below data where Person date of birth field has invalid date")  
@ignore_if_local_run
def valid_batch_file_is_created_with_invalid_person_dateOfBirth_date(datatable, context):  
    build_dataFrame_using_datatable(datatable, context)   
    context.vaccine_df['PERSON_DOB'] = context.vaccine_df['UNIQUE_ID'].apply(lambda uid: get_date(uid.split('-')[1]))     
    create_batch_file(context) 

@then("all records are rejected in the bus ack file and no imms id is generated")
def all_record_are_rejected_for_given_field_name(context):
    all_valid = validate_bus_ack_file_for_error(context)
    assert all_valid, "One or more records failed validation checks"
 