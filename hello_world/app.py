import json
from UnleashClient import UnleashClient
import os
import boto3

def lambda_handler(event, context):

    # Read token value from environment variable
    unleash_token = os.environ["UNLEASH_API_TOKEN"]

    # Create an Unleash client to talk to the Unleash server
    # Toggle values will be written to /tmp for offline access
    client = UnleashClient(
        url="https://eu.app.unleash-hosted.com/eubb1043/api/",
        cache_directory="/tmp",
        app_name="default",
        custom_headers={'Authorization': unleash_token})
    # Initialize the client
    client.initialize_client()

    # If this feature togge is disabled, just return a MOCK value
    if client.is_enabled('grb_toggle') == False:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "sentiment ":  "positive"
            })
        }
    # If not, use AWS comprehend to do sentiment analysis

    comprehend_client  = boto3.client('comprehend')
    ## Extracts BODY from HTTP POST request. Performs Sentiment analysis on the result

    body = event["body"]
    response = comprehend_client.detect_sentiment(LanguageCode = "en", Text = body)

    # Extract sentiment score and label from the response
    sentiment_score = response['SentimentScore']
    sentiment_label = response['Sentiment']

    # Map the sentiment label to a user-friendly description
    sentiment_mapping = {
        'POSITIVE': 'positive',
        'NEGATIVE': 'negative',
        'NEUTRAL': 'neutral',
        'MIXED': 'mixed'
    }
    # Create a user-friendly message

    user_friendly_sentiment = sentiment_mapping[sentiment_label]
    confidence = sentiment_score[user_friendly_sentiment.capitalize()]
    return  {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'sentiment': user_friendly_sentiment,
            'confidence': confidence
        })
    }