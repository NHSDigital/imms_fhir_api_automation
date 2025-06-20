import boto3
import requests
from src.dynamoDB.dynamoDBHelper import *
from src.objectModels.immunization_builder import *
from src.objectModels.patient_loader import load_patient_by_id
from utilities.FHIRImmunizationHelper import *
from utilities.payloadSearch import *
from utilities.payloadCreate import *
from utilities.config import *
from utilities.dynamodbHelper import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
import logging
from pytest_bdd import scenarios, given, when, then, parsers
import pytest_check as check
from features.steps.common_steps import *

config = getConfigParser()


logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)


scenarios("create.feature")

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
    


# @when('Send a create request with POST method for the input JSONs available')
# def createImmsEvent(context):
#     context.createResponse = {}
#     for fileName in context.requestFileName:
#         response = requests.post(context.createUrl, json=context.requestJSON[fileName], headers=context.createHeaders)
#         context.createResponse[fileName] = response


# @then('The create will be successful with the status code 201')
# def validateCreateStatus(context):
#     for fileName in context.requestFileName:
#         statusCode = context.createResponse[fileName].status_code
#         assert statusCode == 201, f"Failed to create immunization event for {fileName}. Status code: {statusCode}. Response: {context.createResponse[fileName].text}"


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
    

@then('The imms event table will be populated with the correct data for the above fields')
def validateImmsEventTable(context):
    create_obj = context.create_object
    created_event= fetchImmsIntImmsEventTable(context.location)
    validateToCompareRequestAndResponse(context, create_obj, created_event)
        
    #     if 'Item' in response:
    #         item = response['Item']
            
    #         identifierPKExpected = context.requestJSON[fileName]['identifier'][0]['system'] + '#' + context.requestJSON[fileName]['identifier'][0]['value']
    #         diseaseType = diseaseTypeMapping(context.requestJSON[fileName])
    #         patientSKExpected = f"{diseaseType}#{context.responseImmsID[fileName]}"
    #         context.requestJSON[fileName]["id"] = context.responseImmsID[fileName]            

    #         with allure.step(f"Validating JSON fields for {fileName} and the immunization event {context.responseImmsID[fileName]}"):
    #             soft_assertions.assert_condition((identifierPKExpected == item['IdentifierPK']), f"Expected IdentifierPK: {identifierPKExpected}, Found: {item['IdentifierPK']}")
    #             soft_assertions.assert_condition(('CREATE'== item['Operation']), f"Expected Operation: CREATE, Found: {item['Operation']}")
    #             soft_assertions.assert_condition((f"Patient#{context.NHSNumber}" == item['PatientPK']), f"Expected Operation: Patient#{context.NHSNumber}, Found: {item['PatientPK']}")
    #             soft_assertions.assert_condition((patientSKExpected == item['PatientSK']), f"Expected IdentifierPK: {patientSKExpected}, Found: {item['PatientSK']}")

    #             if isinstance(item['Resource'], str):
    #                 item['Resource'] = json.loads(item['Resource'])
    #             if isinstance(context.requestJSON[fileName], str):
    #                 context.requestJSON[fileName] = json.loads(context.requestJSON[fileName])  

    #             validate_json_fields(context.requestJSON[fileName], item['Resource'], path="Resource")          
    #     else:
    #         assert False, f"Immunization Event not found in DynamoDB Immunization Event table for {fileName}. Immunization ID: {context.responseImmsID[fileName]}"

    # soft_assertions.assert_all()
