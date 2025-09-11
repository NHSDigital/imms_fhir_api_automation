import requests
import requests
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from src.objectModels.SearchObject import *
from utilities.getHeader import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
import logging
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from features.steps.common_steps import *
from datetime import datetime
from utilities.FHIRImmunizationHelper import *
from datetime import datetime

scenarios("search.feature")

@when('Send a search request with Post method using identifier header for Immunization event created')  
def send_search_post_request_with_identifier_header(context):
    get_search_postURLHeader(context)
    context.request =  {
             "identifier": f'{context.create_object.identifier[0].system}|{context.create_object.identifier[0].value}'
            }
    print(f"\n Search Post Request - \n {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)

@when("Send a search request with GET method for Immunization event created")
def TriggerSearchGetRequest(context):
    get_search_getURLHeader(context)
    context.params = convert_to_form_data(set_request_data(context.patient.identifier[0].value, context.vaccine_type, datetime.today().strftime("%Y-%m-%d")))
    print(f"\n Search Get Parameters - \n {context.params}")
    context.response = requests.get(context.url, params = context.params, headers = context.headers)
    
    print(f"\n Search Get Response - \n {context.response.json()}")

@when("Send a search request with POST method for Immunization event created")
def TriggerSearchPostRequest(context):
    get_search_postURLHeader(context)
    context.request = convert_to_form_data(set_request_data(context.patient.identifier[0].value, context.vaccine_type, datetime.today().strftime("%Y-%m-%d")))
    print(f"\n Search Post Request - \n {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)
    
    print(f"\n Search Post Response - \n {context.response.json()}")

@when(parsers.parse("Send a search request with GET method with invalid NHS Number '{NHSNumber}' and valid Disease Type '{DiseaseType}'"))
@when(parsers.parse("Send a search request with GET method with valid NHS Number '{NHSNumber}' and invalid Disease Type '{DiseaseType}'"))
@when(parsers.parse("Send a search request with GET method with invalid NHS Number '{NHSNumber}' and invalid Disease Type '{DiseaseType}'"))
def send_invalid_param_get_request(context, NHSNumber, DiseaseType):
    get_search_getURLHeader(context)

    if NHSNumber.lower() in ["none", "null", ""]:
        NHSNumber = ""
    if DiseaseType.lower() in ["none", "null", ""]:
        DiseaseType = ""        

    context.NHSNumber = NHSNumber
    context.DiseaseType = DiseaseType
    context.params = convert_to_form_data(set_request_data(NHSNumber, DiseaseType, datetime.today().strftime("%Y-%m-%d")))
    print(f"\n Search Get parameters - \n {context.params}")
    context.response = requests.get(context.url, params = context.params, headers = context.headers)


@when(parsers.parse("Send a search request with POST method with invalid NHS Number '{NHSNumber}' and valid Disease Type '{DiseaseType}'"))
@when(parsers.parse("Send a search request with POST method with valid NHS Number '{NHSNumber}' and invalid Disease Type '{DiseaseType}'"))
@when(parsers.parse("Send a search request with POST method with invalid NHS Number '{NHSNumber}' and invalid Disease Type '{DiseaseType}'"))
def send_invalid_param_post_request(context, NHSNumber, DiseaseType):
    get_search_postURLHeader(context)

    if NHSNumber.lower() in ["none", "null", ""]:
        NHSNumber = ""
    if DiseaseType.lower() in ["none", "null", ""]:
        DiseaseType = ""        

    context.NHSNumber = NHSNumber
    context.DiseaseType = DiseaseType
    context.request = convert_to_form_data(set_request_data(NHSNumber, DiseaseType, datetime.today().strftime("%Y-%m-%d")))
    print(f"\n Search Post request - \n {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)


@when(parsers.parse("Send a search request with GET method with invalid Date From '{DateFrom}' and valid Date To '{DateTo}'"))
@when(parsers.parse("Send a search request with GET method with valid Date From '{DateFrom}' and invalid Date To '{DateTo}'"))
@when(parsers.parse("Send a search request with GET method with invalid Date From '{DateFrom}' and invalid Date To '{DateTo}'"))
def send_invalid_date_get_request(context, DateFrom, DateTo):
    get_search_getURLHeader(context)

    if DateFrom.lower() in ["none", "null", ""]:
        DateFrom = ""
    if DateTo.lower() in ["none", "null", ""]:
        DateTo = ""        

    context.DateFrom = DateFrom
    context.DateTo = DateTo
    context.DiseaseType = "RSV"
    context.NHSNumber = load_patient_by_id("Random").identifier[0].value
    context.params = convert_to_form_data(set_request_data(context.NHSNumber, context.DiseaseType, DateFrom, DateTo))
    print(f"\n Search Get parameters - \n {context.params}")
    context.response = requests.get(context.url, params = context.params, headers = context.headers)


@when(parsers.parse("Send a search request with POST method with invalid Date From '{DateFrom}' and valid Date To '{DateTo}'"))
@when(parsers.parse("Send a search request with POST method with valid Date From '{DateFrom}' and invalid Date To '{DateTo}'"))
@when(parsers.parse("Send a search request with POST method with invalid Date From '{DateFrom}' and invalid Date To '{DateTo}'"))
def send_invalid_param_post_request(context, DateFrom, DateTo):
    get_search_postURLHeader(context)

    if DateFrom.lower() in ["none", "null", ""]:
        DateFrom = ""
    if DateTo.lower() in ["none", "null", ""]:
        DateTo = ""        

    context.DateFrom = DateFrom
    context.DateTo = DateTo
    context.DiseaseType = "COVID19"
    context.NHSNumber = load_patient_by_id("Random").identifier[0].value
    context.request = convert_to_form_data(set_request_data(context.NHSNumber, context.DiseaseType, DateFrom, DateTo))
    print(f"\n Search Post request - \n {context.request}")
    context.response = requests.post(context.url, headers=context.headers, data=context.request)


@when(parsers.parse("Send a search request with GET method with valid NHS Number '{NHSNumber}' and Disease Type '{vaccine_type}' and Date From '{DateFrom}' and Date To '{DateTo}'"))
def send_valid_param_get_request(context, NHSNumber, vaccine_type, DateFrom, DateTo):
    get_search_getURLHeader(context)

    context.DateFrom = DateFrom
    context.DateTo = DateTo
    context.params = convert_to_form_data(set_request_data(NHSNumber, vaccine_type, DateFrom, DateTo))
    print(f"\n Search Get parameters - \n {context.params}")
    context.response = requests.get(context.url, params = context.params, headers = context.headers)

@when(parsers.parse("Send a search request with POST method with valid NHS Number '{NHSNumber}' and Disease Type '{vaccine_type}' and Date From '{DateFrom}' and Date To '{DateTo}'"))
def send_valid_param_post_request(context, NHSNumber, vaccine_type, DateFrom, DateTo):
    get_search_postURLHeader(context)

    context.DateFrom = DateFrom
    context.DateTo = DateTo
    context.request = convert_to_form_data(set_request_data(NHSNumber, vaccine_type, DateFrom, DateTo))
    print(f"\n Search Get parameters - \n {context.request}") 
    context.response = requests.post(context.url, headers=context.headers, data=context.request)  


@then("The occurrenceDateTime of the immunization events should be within the Date From and Date To range")
def validateDateRange(context):
    data = context.response.json()
    context.parsed_search_object = parse_FHIRImmunizationResponse(data)

    assert context.parsed_search_object.entry, "No entries found in the search response."
    
    for entry in context.parsed_search_object.entry:
        if entry.resource.resourceType == "Immunization":
            occurrence_date = entry.resource.occurrenceDateTime
            id = entry.resource.id
            if occurrence_date:
                if context.DateFrom and context.DateTo:
                    occurrence_date = iso_to_compact(occurrence_date)
                    date_from = iso_to_compact(context.DateFrom)
                    date_to = iso_to_compact(context.DateTo)

                    assert date_from <= occurrence_date <= date_to, (
                        f"Occurrence date {occurrence_date} is not within the range Date From {context.DateFrom} and Date To {context.DateTo}. Imms ID: {id}"
                    )   


@then('The Search Response JSONs should contain the detail of the immunization events created above')
def validateImmsID(context):
    data = context.response.json()
    context.parsed_search_object = parse_FHIRImmunizationResponse(data)

    context.created_event = find_entry_by_Imms_id(context.parsed_search_object, context.ImmsID)
   
    if context.created_event is None:
        raise AssertionError(f"No object found with Immunisation ID {context.ImmsID} in the search response.")
    
    patient_reference = getattr(context.created_event.resource.patient, "reference", None)

    if not patient_reference:
        raise ValueError("Patient reference is missing in the found event.")

    # Assign to context for further usage
    context.Patient_fullUrl = patient_reference

@then('The Search Response JSONs field values should match with the input JSONs field values for resourceType Immunization')
def validateJsonImms(context):
    create_obj = context.create_object
    created_event= context.created_event.resource
    validateToCompareRequestAndResponse(context, create_obj, created_event)

@then('The Search Response JSONs field values should match with the input JSONs field values for resourceType Patient')
def validateJsonPat(context):        
    response_patient_entry =  find_patient_by_fullurl(context.parsed_search_object)
    assert response_patient_entry is not None, f"No Patient found with fullUrl {context.Patient_fullUrl}"
    
    response_patient = response_patient_entry.resource
    expected_nhs_number = context.create_object.contained[1].identifier[0].value
    actual_nhs_number = response_patient.identifier[0].value
    expected_system = context.create_object.contained[1].identifier[0].system    
    actual_system = response_patient.identifier[0].system

    fields_to_compare = [
        ("fullUrl", context.Patient_fullUrl, response_patient_entry.fullUrl),

        ("resourceType", "Patient", response_patient.resourceType),
        ("id", expected_nhs_number, response_patient.id),
        ("identifier.system", expected_system, actual_system),
        ("identifier.value", expected_nhs_number, actual_nhs_number),
    ]

    for name, expected, actual in fields_to_compare:
            check.is_true(
                expected == actual,
                f"Expected {name}: {expected}, Actual {actual}"
            )


@then('correct immunization event is returned in the response')
def validate_correct_immunization_event(context):
    data = context.response.json()
    context.parsed_search_object = parse_FHIRImmunizationResponse(data)

    context.created_event = context.parsed_search_object.entry[0] if context.parsed_search_object.entry else None
   
    if context.created_event is None:
        raise AssertionError(f"No object found with Immunisation ID {context.ImmsID} in the search response.")
       
    validateJsonImms(context)
    
    assert context.parsed_search_object.total == 1, "Expected total to be 1, but got {context.parsed_search_object.total}"
