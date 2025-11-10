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

scenarios('batchTests/batch_file_validation.feature')

@given(parsers.parse("batch file is created for below data with {invalid_filename} filename and {file_extension} extension"))
@ignore_if_local_run
def valid_batch_file_is_created_with_details(datatable, context, invalid_filename, file_extension):    
    build_dataFrame_using_datatable(datatable, context)        
    create_batch_file(context,fileName=invalid_filename,file_ext=file_extension)

@then("inf ack file has failure status for processed batch file")
def failed_inf_ack_file(context):  
    all_valid = validate_inf_ack_file(context, success=False)
    assert all_valid, "One or more records failed validation checks"

@then("bus ack file will not be created")
def file_will_not_be_moved_to_destination_bucket(context):
    context.fileContent = wait_and_read_ack_file(context, "forwardedFile", timeout=10)
    assert context.fileContent==None, f"File found in destination bucket: {context.forwarded_prefix}"

@then(parsers.parse("Audit table will have failed status, {queue_name} and {error_details} for the processed batch file"))
def validate_imms_audit_table(context,error_details, queue_name):
    table_query_response = fetch_batch_audit_table_detail(context.aws_profile_name, context.filename, context.S3_env)

    assert isinstance(table_query_response, list) and table_query_response, f"Item not found in response for filename: {context.filename}"
    item = table_query_response[0]
    validate_audit_table_record(context, item, "Failed", error_details, queue_name)       
    update_audit_table_for_failed_status(item,context, context.aws_profile_name, context.S3_env)

# @when("same batch file is uploaded again in s3 bucket")
# def upload_same_batch_file_again(context):
#     upload_file_to_s3_bucket(context, context.filename, context.working_directory, f"immunisation-batch-{context.S3_env}-data-sources")