from utilities.config import *
import uuid

config = getConfigParser()


def get_search_getURLHeader(context):
    context.url = context.baseUrl + "/Immunization"
    context.headers =  {
        'X-Correlation-ID': str(uuid.uuid4()),
        'X-Request-ID': str(uuid.uuid4()),
        'Accept': 'application/fhir+json',
        'Authorization': 'Bearer ' + context.token
        }
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']

def get_search_postURLHeader(context):
    context.url = context.baseUrl + "/Immunization/_search"
    context.headers =  {
        'X-Correlation-ID': str(uuid.uuid4()),
        'X-Request-ID': str(uuid.uuid4()),
        'Accept': 'application/fhir+json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + context.token
        }
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']
    
def get_create_postURLHeader(context):
    context.url = context.baseUrl+ "/Immunization"    
    context.headers = {
        'X-Correlation-ID': str(uuid.uuid4()),
        'X-Request-ID': str(uuid.uuid4()),
        'Accept': 'application/fhir+json',
        'Content-Type': 'application/fhir+json',
        'Authorization': 'Bearer ' + context.token
        }
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']
    
def get_deleteURLHeader(context):
    context.url = context.baseUrl + "/Immunization"    
    context.headers = {
        'X-Correlation-ID': str(uuid.uuid4()),
        'X-Request-ID': str(uuid.uuid4()),
        'Accept': 'application/fhir+json',
        'Content-Type': 'application/fhir+json',
        'Authorization': 'Bearer ' + context.token
        }
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']
    
def get_updateURLHeader(context, tag:str = '1'):
    context.url = context.baseUrl + "/Immunization"    
    context.headers = {
        'X-Correlation-ID': str(uuid.uuid4()),
        'X-Request-ID': str(uuid.uuid4()),
        'Accept': 'application/fhir+json',
        'Content-Type': 'application/fhir+json',
        'E-Tag': tag,
        'Authorization': 'Bearer ' + context.token
        }
    context.corrID = context.headers['X-Correlation-ID']
    context.reqID = context.headers['X-Request-ID']
