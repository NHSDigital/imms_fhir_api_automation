from concurrent.futures import thread
import json
import pandas as pd
import os
from src.dynamoDB.dynamo_db_helper import *
from src.objectModels.api_immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from datetime import datetime, timedelta, timezone
from src.objectModels.batch.batch_file_builder import *
from utilities.batch_S3_buckets import *
from utilities.batch_file_helper import *
from utilities.date_helper import *
from utilities.enums import ActionFlag, Operation
from utilities.vaccination_constants import *
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
import functools

def ignore_if_local_run(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract context from args or kwargs
        context = kwargs.get("context") if "context" in kwargs else (args[-1] if args else None)

        if context and getattr(context, "LOCAL_RUN_WITHOUT_S3_UPLOAD", False):
            print(f"Skipping step '{func.__name__}' due to local execution mode.")
            return None
        return func(*args, **kwargs)
    return wrapper

def ignore_local_run_set_test_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract context from args or kwargs
        context = kwargs.get("context") if "context" in kwargs else (args[-1] if args else None)

        if context and getattr(context, "LOCAL_RUN_WITHOUT_S3_UPLOAD", False):
            print(f"Skipping step '{func.__name__}' due to local execution mode.")

            file_name = os.getenv("LOCAL_RUN_FILE_NAME")
            context.filename = file_name
            context.expected_version = "1"
            file_path = os.path.join(context.working_directory, file_name)

            # Read file into vaccine_df
            try:
                context.vaccine_df = pd.read_csv(
                    file_path,
                    delimiter="|",  # or "," depending on your export logic
                    quotechar='"',
                    dtype=str  # optional: ensures all columns are read as strings
                )
                print(f"Loaded fallback vaccine_df from {file_name}")
            except Exception as e:
                print(f"Failed to load fallback file {file_name}: {e}")
                context.vaccine_df = pd.DataFrame()  # fallback to empty

            return None

        return func(*args, **kwargs)
    return wrapper

@given("batch file is created for below data as full dataset")
@ignore_if_local_run
def valid_batch_file_is_created_with_details(datatable, context):    
    build_dataFrame_using_datatable(datatable, context)        
    create_batch_file(context)

@given("Valid batch file is created")
def valid_batch_file_is_created(context):
    context.file_extension = "csv"
    context.filename = generate_file_name(context) 
    record = build_batch_file(context)
    context.vaccine_df = pd.DataFrame([record.dict()])   
    save_record_to_batch_files_directory(context)
    print(f"Batch file created: {context.filename}")

@when("same batch file is uploaded again in s3 bucket") 
@when("batch file is uploaded in s3 bucket")
@ignore_local_run_set_test_data
def batch_file_upload_in_s3_bucket(context):
    upload_file_to_S3(context)
    print(f"Batch file uploaded to S3: {context.filename}")
    fileIsMoved = wait_for_file_to_move_archive(context)
    assert fileIsMoved, f"File not found in archive after timeout"

# @when("same batch file is uploaded again in s3 bucket")    
# @ignore_local_run_set_test_data
# def same_batch_file_upload_in_s3_bucket(context):
#     time.sleep(30)
#     batch_file_upload_in_s3_bucket(context)
    
@then("file will be moved to destination bucket and inf ack file will be created")
def file_will_be_moved_to_destination_bucket(context):
    context.fileContent = wait_and_read_ack_file(context, "ack")
    assert context.fileContent, f"File not found in destination bucket after timeout:  {context.forwarded_prefix}"
    
@then("inf ack file has success status for processed batch file")
def all_records_are_processed_successfully_in_the_inf_ack_file(context):  
    all_valid = validate_inf_ack_file(context)
    assert all_valid, "One or more records failed validation checks"
    
@then("bus ack file will be created")
def file_will_be_moved_to_destination_bucket(context):
    context.fileContent = wait_and_read_ack_file(context, "forwardedFile")
    assert context.fileContent, f"File not found in destination bucket after timeout: {context.forwarded_prefix}"
    
@then("bus ack will be empty as all records are processed successfully")
def all_records_are_processed_successfully_in_the_batch_file(context): 
    file_rows = read_and_validate_bus_ack_file_content(context) 
    all_valid = validate_bus_ack_file_for_successful_records(context, file_rows)
    assert all_valid, "One or more records failed validation checks"
    
@then("Audit table will have correct status, queue name and record count for the processed batch file")
def validate_imms_audit_table(context):
    table_query_response = fetch_batch_audit_table_detail(context.aws_profile_name, context.filename, context.S3_env)

    assert isinstance(table_query_response, list) and table_query_response, f"Item not found in response for filename: {context.filename}"
    item = table_query_response[0]
    validate_audit_table_record(context, item, "Processed")
    
@then("The delta table will be populated with the correct data for all records in batch file")
def validate_imms_delta_table_for_all_records_in_batch_file(context):
    df = context.vaccine_df

    # Defensive check
    check.is_true("IMMS_ID" in df.columns, "Column 'IMMS_ID' not found in vaccine_df")

    # Filter rows where IMMS_ID is not null
    valid_rows = df[df["IMMS_ID"].notnull()]

    check.is_true(not valid_rows.empty, "No rows with non-null IMMS_ID found in vaccine_df")

    for _, row in valid_rows.iterrows():
        imms_id = row["IMMS_ID"]
        context.ImmsID= imms_id.replace("Immunization#", "")
        batch_record = {k: normalize(v) for k, v in row.to_dict().items()}

        item = fetch_immunization_int_delta_detail_by_immsID(
            context.aws_profile_name,
            context.ImmsID,  
            context.S3_env
        )

        check.is_true(item, f"Item not found in response for IMMS_ID: {imms_id}")

        if item:
            validate_imms_delta_record_with_batch_record(
                context,
                batch_record,
                item,
                Operation.created.value,
                ActionFlag.created.value
            )
            
@then(parsers.parse("The imms event table will be populated with the correct data for '{operation}' event for records in batch file"))
def validate_imms_event_table_for_all_records_in_batch_file(context, operation: Operation):
    df = context.vaccine_df
        
    df["UNIQUE_ID_COMBINED"] = df["UNIQUE_ID_URI"].astype(str) + "#" + df["UNIQUE_ID"].astype(str)
    valid_rows = df[df["UNIQUE_ID_COMBINED"].notnull() & (df["UNIQUE_ID_COMBINED"] != "nan#nan")]

    for idx, row in valid_rows.iterrows():
        unique_id_combined = row["UNIQUE_ID_COMBINED"]
        batch_record = {k: normalize(v) for k, v in row.to_dict().items()}

        table_query_response = fetch_immunization_events_detail_by_IdentifierPK(
            context.aws_profile_name, unique_id_combined, context.S3_env
        )
        assert "Items" in table_query_response and table_query_response["Count"] > 0, \
        f"Item not found in response for unique_id_combined: {unique_id_combined}"

        item = table_query_response["Items"][0]

        df.at[idx, "IMMS_ID"]=  item.get("PK")
        context.ImmsID= item.get("PK").replace("Immunization#", "")

        resource_json_str = item.get("Resource")
        assert resource_json_str, "Resource field missing in item."

        try:
            resource = json.loads(resource_json_str)
        except (TypeError, json.JSONDecodeError) as e:
            print(f"Failed to parse Resource from item: {e}")
            raise AssertionError("Failed to parse Resource from response item.")

        assert resource is not None, "Resource is None in the response"
        created_event = parse_imms_int_imms_event_response(resource)
        
        nhs_number = batch_record.get("NHS_NUMBER") or "TBC"

        fields_to_compare = [
            ("Operation", Operation[operation].value, item.get("Operation")),
            ("SupplierSystem", context.supplier_name, item.get("SupplierSystem")),
            ("PatientPK", f'Patient#{nhs_number}', item.get("PatientPK")),
            ("PatientSK", f"{context.vaccine_type.upper()}#{context.ImmsID}", item.get("PatientSK")),
            ("Version", int(context.expected_version), int(item.get("Version"))),
        ]
        
        for name, expected, actual in fields_to_compare:
            check.is_true(
                    expected == actual,
                    f"Expected {name}: {expected}, Actual {actual}"
                )
            
        validate_to_compare_batch_record_with_event_table_record(context, batch_record, created_event)
    

def normalize(value):
    return "" if pd.isna(value) or value == "" else value

def create_batch_file(context, file_ext: str = "csv", fileName: str = None, delimiter: str = "|"):
    context.expected_version = "1"
    context.FileTimestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + f"{int(datetime.now(timezone.utc).microsecond / 10000):02d}"    
    context.file_extension = file_ext

    timestamp_pattern = r'\d{8}T\d{8}'

    if not fileName:
        context.filename = generate_file_name(context)
    else:
        suffix = "" if re.search(timestamp_pattern, fileName) else f"_{context.FileTimestamp}"
        context.filename = f"{fileName}{suffix}.{context.file_extension}"        
    
    save_record_to_batch_files_directory(context, delimiter)

    print(f"Batch file created: {context.filename}")
    
def build_dataFrame_using_datatable(datatable, context):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    headers = datatable[0]
    rows = datatable[1:]

    table_list = [
        (row[headers.index("patient_id")], f"{row[headers.index('unique_id')]}-{timestamp}")
        for row in rows
    ]    
    records = []
    for patient_id, unique_id in table_list:  
        context.patient_id = patient_id
        record = build_batch_file(context, unique_id=unique_id)
        flat_record = record.dict()
        if "data" in flat_record:
            flat_record = flat_record["data"]
        records.append(flat_record)
    
    context.vaccine_df = pd.DataFrame(records)


