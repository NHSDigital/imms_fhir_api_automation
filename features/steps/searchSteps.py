import requests
import json

from utilities.payloadSearch import *

from behave import *

# import logging
# logging.basicConfig(filename='debugLog.log', level=logging.INFO)
# logger = logging.getLogger(__name__)


@given('After passing all the valid parameters')
def queryParamSearch(context):  
    context.url = searchURL()
    context.params = searchContextParam(context)
    context.headers = searchGETHeaders(context.token)

@when('Send a search request with GET method')
def GETAPISearch(context):
    context.response = requests.get(context.url, params = context.params, headers = context.headers)


@then('The search will be successful with the status code 200')
def APIResponseStatus(context):
    statusCode = context.response.status_code
    assert statusCode == 200


@given('After passing all the valid parameters except an invalid nhsnumber')
def invalidNHSNoSearch(context):
    context.url = searchURL()
    context.params = searchContextParam(context)
    context.headers = searchGETHeaders(context.token)

@then('The search will throw error with the status code 400')
def errorCode4xx(context):
    statusCode = context.response.status_code
    assert statusCode == 400
    # context.soft_assertions.assert_condition(result['MAKE'] == MAKE, f"Make match: {result['MAKE']} = {MAKE}")

@given('Pass the invalid "{NHSNumber}" and valid "{DiseaseType}", "{Include}", "{DateFrom}" & "{DateTo}" parameters')
def invalidNHSNoParamSearch(context,NHSNumber,DiseaseType,Include,DateFrom,DateTo):
    context.url = searchURL()
    context.params = searchPaylodParam(NHSNumber,DiseaseType,Include,DateFrom,DateTo)
    context.headers = searchGETHeaders(context.token)    

