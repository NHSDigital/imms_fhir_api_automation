import time
import boto3
import requests
from utilities.payloadSearch import *
from utilities.payloadCreate import *
from utilities.config import *
from utilities.dynamodbHelper import *
from src.delta.dateValidation import *
from src.delta.deltaHelper import *
# from boto3.dynamodb.conditions import Key, Attr
# from utilities.helper import *

from behave import *

config = getConfigParser()

import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)


@given('Prepare create paylod with "{NHSNumber}", "{birthDate}", "{occurrenceDateTime}", "{recorded}", "{expirationDate}"')
def createData(context,NHSNumber,birthDate,occurrenceDateTime,recorded,expirationDate):
    context.createUrl = createURL()
    context.createPayload = createPayload("NHSNumber,birthDate,occurrenceDateTime,recorded,expirationDate",f"{NHSNumber},{birthDate},{occurrenceDateTime},{recorded},{expirationDate}","create")
    context.createHeaders = createPOSTHeaders(context.token)
    context.corrID = context.createHeaders['X-Correlation-ID']
    context.reqID = context.createHeaders['X-Request-ID']
    context.requestJSON = context.createPayload[0]
    context.requestFileName = context.createPayload[1]
    context.requestTotalFiles = context.createPayload[2]
    context.NHSNumber = NHSNumber
    context.birthDate = birthDate
    context.occurrenceDateTime = occurrenceDateTime
    context.recorded = recorded
    context.expirationDate = expirationDate

@when('Send a create request with POST method for the input JSONs available')
def cretaeImmsEvent(context):
    context.createResponse = {}
    for fileName in context.requestFileName:
        response = requests.post(context.createUrl, json=context.requestJSON[fileName], headers=context.createHeaders)
        context.createResponse[fileName] = response

@then('The create will be successful with the status code 201')
def validateCreateStatus(context):
    for fileName in context.requestFileName:
        statusCode = context.createResponse[fileName].status_code
        assert statusCode == 201, f"Failed to create immunization event for {fileName}. Status code: {statusCode}. Response: {context.createResponse[fileName].text}"

@then('The location key in header will contain the Immunization Id')
def validateCreateLocation(context):
    context.responseImmsID = {}
    for fileName in context.requestFileName:
        statusCode = context.createResponse[fileName].status_code
        location = context.createResponse[fileName].headers['location']
        assert "location" in context.createResponse[fileName].headers, f"Location header is missing in the response for {fileName}. Status code: {statusCode}. Response: {context.createResponse[fileName].text}"
        context.responseImmsID[fileName] = location.split("/")[-1] 

@then('The X-Request-ID and X-Correlation-ID keys in header will populate correctly')
def validateCreateHeader(context):
    for fileName in context.requestFileName:
        
        resCorrId = context.createResponse[fileName].headers['X-Correlation-ID']
        resReqId = context.createResponse[fileName].headers['X-Request-ID']
        assert resCorrId == context.corrID, f"Unexpected X-Correlation-ID: {resCorrId} for {fileName}." 
        assert resReqId == context.reqID, f"Unexpected X-Request-ID: {resReqId} for {fileName}."

@then('The imms event table will be populated with the correct data for the above fields')
def validateImmsEventTable(context):
    context.dynamodb = boto3.resource('dynamodb', region_name=config['dynamoDB']['region'])
    tableImmsEvent = context.dynamodb.Table(config['dynamoDB']['tableName1'])

    for fileName in context.requestFileName:
        
        queryFetch = 'Immunization#' + context.responseImmsID[fileName]
        response = tableImmsEvent.get_item(Key={'PK': queryFetch})
        
        if 'Item' in response:
            item = response['Item']
            
            identifierPKExpected = context.requestJSON[fileName]['identifier'][0]['system'] + '#' + context.requestJSON[fileName]['identifier'][0]['value']
            diseaseType = diseaseTypeMapping(context.requestJSON[fileName])
            patientSKExpected = f"{diseaseType}#{context.responseImmsID[fileName]}"
            context.requestJSON[fileName]["id"] = context.responseImmsID[fileName]            

            with allure.step(f"Validating JSON fields for {fileName} and the immunization event {context.responseImmsID[fileName]}"):
                soft_assertions.assert_condition((identifierPKExpected == item['IdentifierPK']), f"Expected IdentifierPK: {identifierPKExpected}, Found: {item['IdentifierPK']}")
                soft_assertions.assert_condition(('CREATE'== item['Operation']), f"Expected Operation: CREATE, Found: {item['Operation']}")
                soft_assertions.assert_condition((f"Patient#{context.NHSNumber}" == item['PatientPK']), f"Expected Operation: Patient#{context.NHSNumber}, Found: {item['PatientPK']}")
                soft_assertions.assert_condition((patientSKExpected == item['PatientSK']), f"Expected IdentifierPK: {patientSKExpected}, Found: {item['PatientSK']}")

                if isinstance(item['Resource'], str):
                    item['Resource'] = json.loads(item['Resource'])
                if isinstance(context.requestJSON[fileName], str):
                    context.requestJSON[fileName] = json.loads(context.requestJSON[fileName])  

                validate_json_fields(context.requestJSON[fileName], item['Resource'], path="Resource")          
        else:
            assert False, f"Immunization Event not found in DynamoDB Immunization Event table for {fileName}. Immunization ID: {context.responseImmsID[fileName]}"

    soft_assertions.assert_all()


@then('The delta table will be populated with the correct data for the above date fields')
def validateDeltaDates(context):

    tableDelta = context.dynamodb.Table(config['dynamoDB']['tableName2'])

    for fileName in context.requestFileName:
        
        queryDeltaFetch = context.responseImmsID[fileName]
        item = scanDelta(tableDelta,queryDeltaFetch)
        
        if item:
            sorted_items = sorted(item, key=lambda x: x['DateTimeStamp'], reverse=True)
            most_recent_item = sorted_items[0]





            # # logger.info(most_recent_item['Operation'])
            # immsData = most_recent_item['Imms']
            # immsData = immsData[1:-1]
            # immsData = immsData.replace("'", '"')
            # immsData = immsData.split(",")[0]
            # # logger.info(immsData)

            # # immsData = json.loads(immsData)

            # if isinstance(immsData, str):
            #     try:
            #         immsData = json.loads(immsData)
            #     except json.JSONDecodeError as e:
            #         logger.error(f"Invalid JSON string: {immsData}")
            #         logger.error(f"JSONDecodeError: {e}")
            #         raise
            #     logger.info(immsData)
            #     logger.info(immsData['PERSON_DOB'])
          

            # logger.info(1)


            














            birthDateActual = most_recent_item['PERSON_DOB']
            occurrenceDateTimeActual = most_recent_item['DATE_AND_TIME']
            expirationDateActual = most_recent_item['EXPIRY_DATE']
            recordedActual = most_recent_item['RECORDED_DATE']
            birthDateExpected = dateToCSV(context.birthDate)
            occurrenceDateTimeExpected = dateToCSV(context.occurrenceDateTime)
            if context.expirationDate.lower() in ("null", "none", ""):
                expirationDateExpected = ""
            else:
                expirationDateExpected = dateToCSV(context.expirationDate)
            recordedExpected = dateFieldCheck(dateToCSV(context.recorded), "recorded") 

            with allure.step(f"Validating Date fields for {fileName} and the immunization event {context.responseImmsID[fileName]}"):
                soft_assertions.assert_condition((birthDateExpected == birthDateActual), f"Expected birthDate: {birthDateExpected}, Found: {birthDateActual}")
                soft_assertions.assert_condition((occurrenceDateTimeExpected == occurrenceDateTimeActual), f"Expected birthDate: {occurrenceDateTimeExpected}, Found: {occurrenceDateTimeActual}")
                soft_assertions.assert_condition((recordedExpected == recordedActual), f"Expected birthDate: {recordedExpected}, Found: {recordedActual}")
                soft_assertions.assert_condition((expirationDateExpected == expirationDateActual), f"Expected birthDate: {expirationDateExpected}, Found: {expirationDateActual}")

        else:
            assert False, f"Immunization Event not found in DynamoDB Delta table {fileName}. Immunization ID: {context.responseImmsID[fileName]}"
