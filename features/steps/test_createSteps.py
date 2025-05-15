import boto3
import requests
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from utilities.payloadSearch import *
from utilities.payloadCreate import *
from utilities.config import *
from utilities.dynamodbHelper import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
import logging
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check

config = getConfigParser()


logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)


scenarios("create.feature")
#@allure.suite("Create feature")

# @given('Prepare create paylod with "{NHSNumber}", "{birthDate}", "{occurrenceDateTime}", "{recorded}", "{expirationDate}"')
# def createData(context,NHSNumber,birthDate,occurrenceDateTime,recorded,expirationDate):
#     context.createUrl = createURL()
#     context.createPayload = createPayload("NHSNumber,birthDate,occurrenceDateTime,recorded,expirationDate",f"{NHSNumber},{birthDate},{occurrenceDateTime},{recorded},{expirationDate}","create")
#     context.createHeaders = createPOSTHeaders(context.token)
#     context.corrID = context.createHeaders['X-Correlation-ID']
#     context.reqID = context.createHeaders['X-Request-ID']
#     context.requestJSON = context.createPayload[0]
#     context.requestFileName = context.createPayload[1]
#     context.requestTotalFiles = context.createPayload[2]
#     context.NHSNumber = NHSNumber
#     context.birthDate = birthDate
#     context.occurrenceDateTime = occurrenceDateTime
#     context.recorded = recorded
#     context.expirationDate = expirationDate
    

@given("Valid json payload is created")
def valid_json_payload_is_created(context):
    context.patient = load_patient_by_id(context.patient_id)
    context.immunization_object = create_immunization_object(context.patient, context.vaccine_type)
    
@when("Trigger the post create request")
def Trigger_the_post_create_request(context):
    context.url = createURL(context.baseUrl)
    context.headers = createPOSTHeaders(context.token)
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']
    context.request = to_clean_dict(asdict(context.immunization_object))
    context.response = requests.post(context.url, json=context.request, headers=context.headers)
    print(f"Create Request is {json.dumps(context.request)}" )

# @when('Send a create request with POST method for the input JSONs available')
# def createImmsEvent(context):
#     context.createResponse = {}
#     for fileName in context.requestFileName:
#         response = requests.post(context.createUrl, json=context.requestJSON[fileName], headers=context.createHeaders)
#         context.createResponse[fileName] = response

@then(parsers.parse("The request will be successful with the status code '{statusCode:d}'"))
def The_request_will_be_successful_with_the_status_code(context, statusCode):
    assert context.response.status_code == statusCode

# @then('The create will be successful with the status code 201')
# def validateCreateStatus(context):
#     for fileName in context.requestFileName:
#         statusCode = context.createResponse[fileName].status_code
#         assert statusCode == 201, f"Failed to create immunization event for {fileName}. Status code: {statusCode}. Response: {context.createResponse[fileName].text}"

@then('The location key in header will contain the Immunization Id')
def validateCreateLocation(context):
    location = context.response.headers['location']
    assert  "location" in context.response.headers, f"Location header is missing in the response with Status code: {context.response.statusCode}. Response: {context.response.json()}"
    context.ImmsID = location.split("/")[-1]
    check.is_true(
        context.ImmsID is not None, 
        f"Expected IdentifierPK: {context.patient.identifier[0].value}, Found: {context.ImmsID}"
    )
    # context.responseImmsID = {}
    # for fileName in context.requestFileName:
    #     statusCode = context.createResponse[fileName].status_code
    #     location = context.createResponse[fileName].headers['location']
    #     assert "location" in context.createResponse[fileName].headers, f"Location header is missing in the response for {fileName}. Status code: {statusCode}. Response: {context.createResponse[fileName].text}"
    #     context.responseImmsID[fileName] = location.split("/")[-1] 

@then('The X-Request-ID and X-Correlation-ID keys in header will populate correctly')
def validateCreateHeader(context):
    assert "X-Request-ID" in context.response.request.headers, "X-Request-ID missing in headers"
    assert "X-Correlation-ID" in context.response.request.headers, "X-Correlation-ID missing in headers"
    assert context.response.request.headers["X-Request-ID"] == context.reqID, "X-Request-ID incorrect"
    assert context.response.request.headers["X-Correlation-ID"] == context.corrID, "X-Correlation-ID incorrect"
    # for fileName in context.requestFileName:
        
    #     resCorrId = context.createResponse[fileName].headers['X-Correlation-ID']
    #     resReqId = context.createResponse[fileName].headers['X-Request-ID']
    #     assert resCorrId == context.corrID, f"Unexpected X-Correlation-ID: {resCorrId} for {fileName}." 
    #     assert resReqId == context.reqID, f"Unexpected X-Request-ID: {resReqId} for {fileName}."

# @then('The imms event table will be populated with the correct data for the above fields')
# def validateImmsEventTable(context):
#     context.dynamodb = boto3.resource('dynamodb', region_name=config['dynamoDB']['region'])
#     tableImmsEvent = context.dynamodb.Table(config['dynamoDB']['tableName1'])

#     for fileName in context.requestFileName:
        
#         queryFetch = 'Immunization#' + context.responseImmsID[fileName]
#         response = tableImmsEvent.get_item(Key={'PK': queryFetch})
        
#         if 'Item' in response:
#             item = response['Item']
            
#             identifierPKExpected = context.requestJSON[fileName]['identifier'][0]['system'] + '#' + context.requestJSON[fileName]['identifier'][0]['value']
#             diseaseType = diseaseTypeMapping(context.requestJSON[fileName])
#             patientSKExpected = f"{diseaseType}#{context.responseImmsID[fileName]}"
#             context.requestJSON[fileName]["id"] = context.responseImmsID[fileName]            

#             with allure.step(f"Validating JSON fields for {fileName} and the immunization event {context.responseImmsID[fileName]}"):
#                 soft_assertions.assert_condition((identifierPKExpected == item['IdentifierPK']), f"Expected IdentifierPK: {identifierPKExpected}, Found: {item['IdentifierPK']}")
#                 soft_assertions.assert_condition(('CREATE'== item['Operation']), f"Expected Operation: CREATE, Found: {item['Operation']}")
#                 soft_assertions.assert_condition((f"Patient#{context.NHSNumber}" == item['PatientPK']), f"Expected Operation: Patient#{context.NHSNumber}, Found: {item['PatientPK']}")
#                 soft_assertions.assert_condition((patientSKExpected == item['PatientSK']), f"Expected IdentifierPK: {patientSKExpected}, Found: {item['PatientSK']}")

#                 if isinstance(item['Resource'], str):
#                     item['Resource'] = json.loads(item['Resource'])
#                 if isinstance(context.requestJSON[fileName], str):
#                     context.requestJSON[fileName] = json.loads(context.requestJSON[fileName])  

#                 validate_json_fields(context.requestJSON[fileName], item['Resource'], path="Resource")          
#         else:
#             assert False, f"Immunization Event not found in DynamoDB Immunization Event table for {fileName}. Immunization ID: {context.responseImmsID[fileName]}"

#     soft_assertions.assert_all()


# @then('The delta table will be populated with the correct data for the above date fields')
# def validateDeltaDates(context):

#     tableDelta = context.dynamodb.Table(config['dynamoDB']['tableName2'])

#     for fileName in context.requestFileName:
        
#         queryDeltaFetch = context.responseImmsID[fileName]
#         item = scanDelta(tableDelta,queryDeltaFetch)
        
#         if item:
#             sorted_items = sorted(item, key=lambda x: x['DateTimeStamp'], reverse=True)
#             most_recent_item = sorted_items[0]
#             # # logger.info(most_recent_item['Operation'])
#             # immsData = most_recent_item['Imms']
#             # immsData = immsData[1:-1]
#             # immsData = immsData.replace("'", '"')
#             # immsData = immsData.split(",")[0]
#             # # logger.info(immsData)

#             # # immsData = json.loads(immsData)

#             # if isinstance(immsData, str):
#             #     try:
#             #         immsData = json.loads(immsData)
#             #     except json.JSONDecodeError as e:
#             #         logger.error(f"Invalid JSON string: {immsData}")
#             #         logger.error(f"JSONDecodeError: {e}")
#             #         raise
#             #     logger.info(immsData)
#             #     logger.info(immsData['PERSON_DOB'])
          

#             # logger.info(1)
#             birthDateActual = most_recent_item['PERSON_DOB']
#             occurrenceDateTimeActual = most_recent_item['DATE_AND_TIME']
#             expirationDateActual = most_recent_item['EXPIRY_DATE']
#             recordedActual = most_recent_item['RECORDED_DATE']
#             birthDateExpected = dateToCSV(context.birthDate)
#             occurrenceDateTimeExpected = dateToCSV(context.occurrenceDateTime)
#             if context.expirationDate.lower() in ("null", "none", ""):
#                 expirationDateExpected = ""
#             else:
#                 expirationDateExpected = dateToCSV(context.expirationDate)
#             recordedExpected = dateFieldCheck(dateToCSV(context.recorded), "recorded") 

#             with allure.step(f"Validating Date fields for {fileName} and the immunization event {context.responseImmsID[fileName]}"):
#                 soft_assertions.assert_condition((birthDateExpected == birthDateActual), f"Expected birthDate: {birthDateExpected}, Found: {birthDateActual}")
#                 soft_assertions.assert_condition((occurrenceDateTimeExpected == occurrenceDateTimeActual), f"Expected birthDate: {occurrenceDateTimeExpected}, Found: {occurrenceDateTimeActual}")
#                 soft_assertions.assert_condition((recordedExpected == recordedActual), f"Expected birthDate: {recordedExpected}, Found: {recordedActual}")
#                 soft_assertions.assert_condition((expirationDateExpected == expirationDateActual), f"Expected birthDate: {expirationDateExpected}, Found: {expirationDateActual}")

#         else:
#             assert False, f"Immunization Event not found in DynamoDB Delta table {fileName}. Immunization ID: {context.responseImmsID[fileName]}"
