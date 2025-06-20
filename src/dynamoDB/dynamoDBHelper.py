import boto3

def fetchImmsIntImmsEventTable(ImmsID:str):    
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
        tableImmsEvent = dynamodb.Table('imms-int-imms-events')

        queryFetch = f"Immunization#{ImmsID}"

        response = tableImmsEvent.get_item(Key={'PK': queryFetch})
        print(f"response is {response}")
    