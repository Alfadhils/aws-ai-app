import json
import boto3
import base64

# Initialize the Polly client
polly = boto3.client('polly')

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)

        text = body["text"]
        language_code = body["language_code"]
        voice_id = body["voice_id"]
        engine = body["engine"]

        # Use Polly to synthesize speech
        response = polly.synthesize_speech(
            Text=text,
            Engine=engine,
            OutputFormat="mp3",
            VoiceId=voice_id,
            LanguageCode=language_code
        )

        # Read binary stream
        audio_stream = response["AudioStream"].read()
        audio_base64 = base64.b64encode(audio_stream).decode("utf-8")

        return {
            "statusCode": 200,
            "body": json.dumps({"audio_base64": audio_base64})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
