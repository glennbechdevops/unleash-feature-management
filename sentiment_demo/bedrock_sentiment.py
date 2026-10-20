import json
import os
import re

import boto3


def analyze(text):
    """Classify sentiment with Bedrock and return label, confidence, and reasoning."""
    client = boto3.client('bedrock-runtime')
    # Current Claude models on Bedrock require a regional inference profile,
    # not a raw foundation-model ID.
    model_id = os.environ.get(
        'BEDROCK_MODEL_ID',
        'eu.anthropic.claude-haiku-4-5-20251001-v1:0'
    )

    prompt = (
        "Classify the sentiment of the text below as one of: "
        "positive, negative, neutral, mixed.\n\n"
        "Reply with ONLY a JSON object (no markdown, no commentary) with keys:\n"
        "  - sentiment: one of the four words above, lowercase\n"
        "  - confidence: a number between 0 and 1\n"
        "  - reasoning: a short sentence justifying the rating\n\n"
        f"Text: {text}"
    )

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}]
    })

    response = client.invoke_model(modelId=model_id, body=body)
    payload = json.loads(response['body'].read())
    reply = payload['content'][0]['text'].strip()

    # Claude often wraps JSON in ```json fences even when told not to.
    match = re.search(r'\{.*\}', reply, re.DOTALL)
    parsed = json.loads(match.group(0) if match else reply)

    return {
        "sentiment": parsed['sentiment'],
        "confidence": parsed['confidence'],
        "reasoning": parsed['reasoning'],
    }
