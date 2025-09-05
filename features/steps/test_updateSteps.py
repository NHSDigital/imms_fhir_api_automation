import requests
import requests
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.SearchObject import *
from utilities.enums import ActionFlag
from utilities.getHeader import *
from utilities.config import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
import logging
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from features.steps.common_steps import *
from datetime import datetime
from utilities.FHIRImmunizationHelper import *
from datetime import datetime



config = getConfigParser()


logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

scenarios("update.feature")

@when('Send a update for Immunization event created with patient address being updated')
def send_update_for_immunization_event(context):
    get_updateURLHeader(context, str(context.expected_version))
    context.update_object = convert_to_update(context.immunization_object, context.ImmsID)
    context.expected_version = int(context.expected_version) + 1
    context.update_object.contained[1].address[0].city = "Updated City"
    context.update_object.contained[1].address[0].state = "Updated State"
    context.create_object = context.update_object
    context.request = context.update_object.dict(exclude_none=True, exclude_unset=True)
    context.response = requests.put(context.url + "/" + context.ImmsID, json=context.request, headers=context.headers)
    print(f"Update Request is {json.dumps(context.request)}" )
    
@when(parsers.parse("Send a update for Immunization event created with patient address being updated by '{Supplier}'"))
def send_update_for_immunization_event_by_supplier(context, Supplier):
    valid_token_is_generated(context, Supplier)
    send_update_for_immunization_event(context)
    
@when('Send a update for Immunization event created with vaccination detail being updated')
def send_update_for_vaccination_detail(context):
    get_updateURLHeader(context, str(context.expected_version))
    context.update_object = convert_to_update(context.immunization_object, context.ImmsID)
    context.expected_version = int(context.expected_version) + 1
    context.update_object.extension = [build_vaccine_procedure_extension(context.vaccine_type.upper())]
    vaccine_details = get_vaccine_details(context.vaccine_type.upper())
    context.update_object.vaccineCode = vaccine_details["vaccine_code"]
    context.update_object.site = build_site_route(random.choice(SITE_MAP))
    context.update_object.route = build_site_route(random.choice(ROUTE_MAP))
    context.create_object = context.update_object
    context.request = context.update_object.dict(exclude_none=True, exclude_unset=True)
    context.response = requests.put(context.url + "/" + context.ImmsID, json=context.request, headers=context.headers)
    print(f"Update Request is {json.dumps(context.request)}" )
    
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
    