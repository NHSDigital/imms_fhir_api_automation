import pandas as pd
import pytest
from src.dynamoDB.dynamoDBHelper import *
from src.objectModels.api_immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from datetime import datetime, timedelta, timezone
from src.objectModels.batch.batch_file_builder import *
from utilities.batch_S3_buckets import *
from utilities.batch_file_helper import validate_forwarded_file
from utilities.date_helper import *
from utilities.vaccination_constants import *
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check

scenarios('batchTests/create_batch.feature')
table_map= {}

@given("Valid batch file is created")
def valid_batch_file_is_created(context):
    context.file_extension = "csv"
    context.filename = generate_file_name(context)
    record = build_batch_file(context)
    context.vaccine_df = pd.DataFrame([record.dict()])   
    save_record_to_batch_files_directory(context)
    print(f"✅ Batch file created: {context.filename}")
    
    
@given("batch file is created for below data")
def valid_batch_file_is_created_with_details(datatable, context):
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

    # datatable is a list of lists: first row is headers
    headers = datatable[0]
    rows = datatable[1:]
    # Build table_map from rows
    table_map = {
        row[headers.index("patient_id")]: f"{row[headers.index('unique_id')]}_{timestamp}"
        for row in rows
    }
    context.file_extension = "csv"
    context.filename = generate_file_name(context)

    records = []
    for patient_id, unique_id in table_map.items():
        context.patient_id = patient_id
        record = build_batch_file(context, unique_id=unique_id)
        flat_record = record.dict()
        if "data" in flat_record:
            flat_record = flat_record["data"]
        records.append(flat_record)
        
    context.vaccine_df = pd.DataFrame(records)
    print(context.vaccine_df)
    print(len(context.vaccine_df))
    save_record_to_batch_files_directory(context)

    print(f"✅ Batch file created: {context.filename}")

    
@when("batch file upload in s3 bucket")
def batch_file_upload_in_s3_bucket(context):
    upload_file_to_S3(context)
    print(f"✅ Batch file uploaded to S3: {context.filename}")
    fileIsMoved = wait_for_file_to_move_archive(context)
    assert fileIsMoved, f"File not found in archive after timeout: {context.archive_key}"
    
@then("file will be moved to destination bucket")
def file_will_be_moved_to_destination_bucket(context):
    context.fileContent = wait_and_read_forwarded_file(context)
    assert context.fileContent, f"File not found in destination bucket after timeout: {context.forwarded_prefix}"
    
@then("all records are processed successfully in the batch file")
def all_records_are_processed_successfully_in_the_batch_file(context):  
    all_valid = validate_forwarded_file(context)
    assert all_valid, "One or more records failed validation checks"
    print("✅ All records processed successfully in the batch file")