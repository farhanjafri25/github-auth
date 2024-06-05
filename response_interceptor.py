import json

def format_response(status_code, data=None):
    response = {
        "statusCode": status_code,
        "body": {"data": data}
    }
    print('response', response)
    return response
