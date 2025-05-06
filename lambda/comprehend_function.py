import json
import boto3

# Initialize the Comprehend client
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        
        text = body["text"]
        language_code = "en"

        # Use Comprehend to detect entities
        entities_response = comprehend.detect_entities(Text=text, LanguageCode=language_code)
        entities = entities_response.get('Entities', [])

        # Use Comprehend to detect sentiment
        sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
        sentiment = sentiment_response.get('Sentiment')
        sentiment_score = sentiment_response.get('SentimentScore', {})

        return {
            'statusCode': 200,
            'body': json.dumps({
                'entities': entities,
                'sentiment': sentiment,
                'sentiment_score': sentiment_score
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({ "error": str(e) })
        }
