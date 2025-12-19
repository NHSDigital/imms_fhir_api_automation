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
from features.APITests.steps.common_steps import *
from features.APITests.steps.test_create_steps import validate_imms_delta_table_by_ImmsID
from features.APITests.steps.test_update_steps import validate_delta_table_for_updated_event

scenarios('batchTests/delete_batch.feature')

@given("batch file is created for below data as full dataset and each record has a valid delete record in the same file")
@ignore_if_local_run
def valid_batch_file_is_created_with_details(datatable, context):    
    build_dataFrame_using_datatable(datatable, context) 
    df_new = context.vaccine_df.copy()
    df_update = df_new.copy()
    df_update["ACTION_FLAG"] = "DELETE"
    context.vaccine_df = pd.concat([df_new, df_update], ignore_index=True)      
    create_batch_file(context)