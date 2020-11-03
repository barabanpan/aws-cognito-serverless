import json

from decorators import log_request


@log_request
def subtract(event, context):
    args = json.loads(event['body'])
    a, b = args.get('a'), args.get('b')
    res = eval(f'{a} - {b}')

    return {
        'statusCode': 200,
        'body': json.dumps({'res': res})
    }
