import requests
import requests
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.SearchObject import *
from utilities.enums import ActionFlag
from utilities.getHeader import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from features.steps.common_steps import *
from datetime import datetime
from utilities.FHIRImmunizationHelper import *
from datetime import datetime

scenarios("update.feature")

   
@when(parsers.parse("Send a update for Immunization event created with patient address being updated by '{Supplier}'"))
def send_update_for_immunization_event_by_supplier(context, Supplier):
    valid_token_is_generated(context, Supplier)
    send_update_for_immunization_event(context)
    
    
@then('The delta table will be populated with the correct data for updated event')
def validate_delta_table_for_updated_event(context):
    create_obj = context.create_object
    items = fetch_immunization_int_delta_detail_by_immsID(context.aws_profile_name, context.ImmsID)
    assert items, f"Items not found in response for ImmsID: {context.ImmsID}"

    # Find the latest item where operation is updated
    delta_items = [i for i in items if i.get('Operation') == Operation.updated.value ]
    
    assert delta_items, f"No item found for ImmsID: {context.ImmsID}"

    item = [max(delta_items, key=lambda x: x.get('DateTimeStamp', 0))]
     
    validate_imms_delta_record_with_created_event(context, create_obj, item, Operation.updated.value, ActionFlag.updated.value)    