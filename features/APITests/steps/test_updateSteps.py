import requests
from src.objectModels.api_immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.api_search_object import *
from utilities.enums import ActionFlag
from utilities.api_get_header import *
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from ..steps.common_steps import *
from utilities.api_fhir_immunization_helper import *
from utilities.date_helper import *

scenarios('APITests/update.feature')

   
@when(parsers.parse("Send a update for Immunization event created with patient address being updated by '{Supplier}'"))
def send_update_for_immunization_event_by_supplier(context, Supplier):
    valid_token_is_generated(context, Supplier)
    send_update_for_immunization_event(context)
    
    
@then('The delta table will be populated with the correct data for updated event')
def validate_delta_table_for_updated_event(context):
    create_obj = context.create_object
    items = fetch_immunization_int_delta_detail_by_immsID(context.aws_profile_name, context.ImmsID, context.S3_env)
    assert items, f"Items not found in response for ImmsID: {context.ImmsID}"
    delta_items = [i for i in items if i.get('Operation') == Operation.updated.value ]    
    assert delta_items, f"No item found for ImmsID: {context.ImmsID}"
    item = [max(delta_items, key=lambda x: x.get('DateTimeStamp', 0))]     
    validate_imms_delta_record_with_created_event(context, create_obj, item, Operation.updated.value, ActionFlag.updated.value)
    
@when(parsers.parse("Send a update for Immunization event created with occurrenceDateTime being updated to '{DateText}'"))
def send_update_for_immunization_event_with_occurrenceDateTime(context, DateText):
    get_updateURLHeader(context, str(context.expected_version))
    context.update_object = convert_to_update(context.immunization_object, context.ImmsID)
    context.update_object.occurrenceDateTime = generate_date(DateText)
    trigger_the_updated_request(context)
    
@when(parsers.parse("Send a update for Immunization event created with recorded being updated to '{DateText}'"))
def send_update_for_immunization_event_with_occurrenceDateTime(context, DateText):
    get_updateURLHeader(context, str(context.expected_version))
    context.update_object = convert_to_update(context.immunization_object, context.ImmsID)
    context.update_object.recorded = generate_date(DateText)
    trigger_the_updated_request(context)
    
    
@when(parsers.parse("Send a update for Immunization event created with patient date of bith being updated to '{DateText}'"))
def send_update_for_immunization_event_with_occurrenceDateTime(context, DateText):
    get_updateURLHeader(context, str(context.expected_version))
    context.update_object = convert_to_update(context.immunization_object, context.ImmsID)
    context.update_object.contained[1].birthDate = generate_date(DateText)
    trigger_the_updated_request(context)
    
@when(parsers.parse("Send a update for Immunization event created with expiration date being updated to '{DateText}'"))
def send_update_for_immunization_event_with_occurrenceDateTime(context, DateText):
    get_updateURLHeader(context, str(context.expected_version))
    context.update_object = convert_to_update(context.immunization_object, context.ImmsID)
    context.update_object.expirationDate = generate_date(DateText)
    trigger_the_updated_request(context)
    