from boto3.dynamodb.conditions import Key, Attr

def scanDelta(tableDelta,queryDeltaFetch):
    items = []
    response = tableDelta.scan(FilterExpression=Attr('ImmsID').eq(queryDeltaFetch))
    items.extend(response.get('Items', []))

    while 'LastEvaluatedKey' in response:
        response = tableDelta.scan(
            FilterExpression=Attr('ImmsID').eq(queryDeltaFetch),
                    ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response.get('Items', []))

    if items:
        return items  