from utilities.config import *
from utilities.resources import apiResources

configUrl = getConfigParser()

def searchURL():
    url = configUrl['API']['baseUrl'] + apiResources.createEndpoint
    return url

# def searchPaylod():
    
#     patID = "https://fhir.nhs.uk/Id/nhs-number|9449310610"
#     immTgt = "COVID19, FLU, RSV"
#     incl = "Immunization:patient"
#     dtF = None
#     dtT = None

#     searchParams={'patient.identifier': patID, '-immunization.target' : immTgt, '_include' : incl, '-date.from' : dtF, '-date.to' : dtT}
#     return searchParams

def searchContextParam(parameters):
    for row in parameters.table:
        NHSNumber = row['NHSNumber']
        DiseaseType = row['DiseaseType']
        Include = row['Include']
        DateFrom = row['DateFrom']
        DateTo = row['DateTo']

    if (DateFrom == "None" or DateFrom == "") and (DateTo == "None" or DateTo == ""):
        searchParams={'patient.identifier': configUrl['API']['FHIRNHSNumber'] + NHSNumber, '-immunization.target' : DiseaseType, '_include' : Include}
    else:
        searchParams={'patient.identifier': configUrl['API']['FHIRNHSNumber'] + NHSNumber, '-immunization.target' : DiseaseType, '_include' : Include, '-date.from' : DateFrom, '-date.to' : DateTo}

    return searchParams

def searchPaylodParam(patID,immTgt,incl,dtF,dtT):
    
    patID = configUrl['API']['FHIRNHSNumber'] + patID
    searchParams={'patient.identifier': patID, '-immunization.target' : immTgt, '_include' : incl, '-date.from' : dtF, '-date.to' : dtT}
    return searchParams

def searchGETHeaders():
    corID = "bc6A545e-028C-2aE4-0acF-38aDD0134f9f"
    reqID = "bc6A545e-028C-2aE4-0acF-38aDD0134f9f"
    searchHeaders = {
        'X-Correlation-ID': corID,
        'X-Request-ID': reqID,
        'Accept': 'application/fhir+json',
        'Authorization': 'Bearer Iy3KWA2Z3coGgRO8LCT2Ai9eJ9IJ'
        }
    return searchHeaders


