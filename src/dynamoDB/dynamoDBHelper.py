import boto3
from boto3.dynamodb.conditions import Attr
from botocore.config import Config

from src.objectModels.dataObjects import ImmunizationIntTable

my_config = Config(
    region_name='eu-west-2',
    connect_timeout=10,  # seconds to wait for connection
    read_timeout=30     # seconds to wait for a response
)


def fetch_immunization_events_detail(ImmsID: str):
    dynamodb = boto3.resource('dynamodb',  config=my_config)
    tableImmsEvent = dynamodb.Table('imms-int-imms-events') # type: ignore

    queryFetch = f"Immunization#{ImmsID}"

    response = tableImmsEvent.get_item(Key={'PK': queryFetch})
    print(f"\n response is {response} \n")

    return response
    
def parse_imms_int_imms_event_response(json_data: dict) -> ImmunizationIntTable:
    return ImmunizationIntTable.parse_obj(json_data)  

def fetch_immunization_int_delta_detail_by_immsID(ImmsID: str):
    dynamodb = boto3.resource('dynamodb', config=my_config)
    tableImmsDelta = dynamodb.Table('imms-int-delta') # type: ignore

    for segment in range(4):
        response = tableImmsDelta.scan(
            FilterExpression=Attr('ImmsID').eq(ImmsID),
            TotalSegments=4,
            Segment=segment
    )

    print(f"\n response is {response} \n")

    return response