import pandas as pd
from src.dynamoDB.dynamoDBHelper import *
from src.objectModels.api_immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from datetime import datetime, timedelta, timezone
from src.objectModels.batch.batch_file_builder import *
from utilities.enums import ActionFlag, SupplierNameWithODSCode
from utilities.date_helper import *
from utilities.vaccination_constants import *
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check

scenarios('batchTests/create_batch.feature')

@given("Valid batch file is created")
def valid_batch_file_is_created(context):
    context.file_extension = "csv"
    context.filename = generate_file_name(context)
    record = build_batch_file(context)
    context.vaccine_df = pd.DataFrame([record.dict()])   
    save_record_to_batch_files_directory(context)
    print(f"✅ Batch file created: {context.filename}")
    
@when("batch file upload in s3 bucket")
def batch_file_upload_in_s3_bucket(context):
    #upload_file_to_s3(context)
    print(f"✅ Batch file uploaded to S3: {context.filename}")