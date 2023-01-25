import json
from UnleashClient import UnleashClient
import os

def lambda_handler(event, context):

    print ("start")

    unleash_token = os.environ["UNLEASH_API_TOKEN"]

    client = UnleashClient(
        url="https://eu.app.unleash-hosted.com/eubb1043/api/",
        app_name="default",
        custom_headers={'Authorization': unleash_token})
    client.initialize_client()

    not_implemented_response = {
        "statusCode": 501,
        "body": json.dumps({
            "message": "Not yet implemented",
        }),
    }

    ok_response =  {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }

    if client.is_enabled('glenn_toggle'):
        return ok_response
    else:
        return not_implemented_response
