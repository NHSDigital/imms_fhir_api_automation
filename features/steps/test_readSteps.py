import requests
import requests
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.SearchObject import *
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

scenarios("read.feature")

@when("Send a read request for Immunization event created")
def send_read_for_immunization_event_created(context):
    get_readURLHeader(context)
    print(f"\n Read Request is {context.url}")
    context.response = requests.get(f"{context.url}", headers=context.headers)
    
@then("The Read Response JSONs field values should match with the input JSONs field values")
def the_read_response_jsons_field_values_should_match_with_the_input_jsons_field_values(context):
    create_obj = context.create_object
    data = context.response.json()
    context.created_event = parse_readResponse(data)
    validateToCompareRequestAndResponse(context, create_obj, context.created_event , True)