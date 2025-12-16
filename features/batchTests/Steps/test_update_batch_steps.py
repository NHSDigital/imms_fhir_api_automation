from multiprocessing import context
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

scenarios('batchTests/update_batch.feature')

@given("batch file is created for below data as full dataset and each record has a valid update record in te same file")
@ignore_if_local_run
def valid_batch_file_is_created_with_details(datatable, context):    
    build_dataFrame_using_datatable(datatable, context) 
    df_new = context.vaccine_df.copy()
    df_update = df_new.copy()
    df_update[["ACTION_FLAG", "EXPIRY_DATE"]] = ["UPDATE", "20281231"]
    context.vaccine_df = pd.concat([df_new, df_update], ignore_index=True) 
    context.expected_version = 2      
    create_batch_file(context)