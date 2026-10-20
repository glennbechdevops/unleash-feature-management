import boto3


SENTIMENT_MAPPING = {
    'POSITIVE': 'positive',
    'NEGATIVE': 'negative',
    'NEUTRAL': 'neutral',
    'MIXED': 'mixed',
}


def analyze(text):
    """Classify sentiment with AWS Comprehend and return label and confidence."""
    client = boto3.client('comprehend')
    response = client.detect_sentiment(LanguageCode="en", Text=text)
    label = SENTIMENT_MAPPING[response['Sentiment']]
    confidence = response['SentimentScore'][label.capitalize()]
    return {"sentiment": label, "confidence": confidence}
