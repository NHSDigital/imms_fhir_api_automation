import requests
import json

from utilities.payload import *

from behave import *

@given('After passing all the valid parameters')
def queryParamSearch(context):
    context.url = searchURL()
    context.params = searchContextParam(context)
    context.headers = searchGETHeaders()

@when('Send a search request with GET method')
def GETAPISearch(context):
    context.response = requests.get(context.url, params = context.params, headers = context.headers)


@then('The search will be successful with the status code 200')
def APIResponseStatus(context):
    statusCode = context.response.status_code
    # print(context.response.status_code)
    # print(context.response.text)
    assert statusCode == 200


@given('After passing all the valid parameters except an invalid nhsnumber')
def invalidNHSNoSearch(context):
    context.url = searchURL()
    context.params = searchContextParam(context)
    context.headers = searchGETHeaders()

@then('The search will be throw error with the status code 400')
def errorCode4xx(context):
    statusCode = context.response.status_code
    # print(context.response.status_code)
    assert statusCode == 400

@given('Pass the invalid "{NHSNumber}" and valid "{DiseaseType}", "{Include}", "{DateFrom}" & "{DateTo}" parameters')
def invalidNHSNoParamSearch(context,NHSNumber,DiseaseType,Include,DateFrom,DateTo):
    context.url = searchURL()
    context.params = searchPaylodParam(NHSNumber,DiseaseType,Include,DateFrom,DateTo)
    context.headers = searchGETHeaders()    

