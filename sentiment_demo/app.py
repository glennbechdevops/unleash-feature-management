import json
import os

from UnleashClient import UnleashClient

import bedrock_sentiment
import comprehend_sentiment


def lambda_handler(event, context):
    unleash_token = os.environ["UNLEASH_API_TOKEN"]

    client = UnleashClient(
        url="https://eu.app.unleash-hosted.com/eubb1043/api/",
        cache_directory="/tmp",
        app_name="default",
        custom_headers={'Authorization': unleash_token})
    client.initialize_client()

    # Toggle picks the sentiment backend:
    # On  → Bedrock (adds a 'reasoning' field)
    # Off → Comprehend
    if client.is_enabled('grb_toggle'):
        result = bedrock_sentiment.analyze(event["body"])
    else:
        result = comprehend_sentiment.analyze(event["body"])


    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
