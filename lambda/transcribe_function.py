import json
import boto3
import base64
import uuid
import os

# Initialize the S3 and Transcribe clients
s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

# Get the bucket name from environment variables
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        
        
        audio_base64 = body['audio_base64']
        audio_bytes = base64.b64decode(audio_base64)
        
        # Generate a unique file name for the audio
        file_id = str(uuid.uuid4())
        file_name = f"{file_id}.mp3"
        s3_key = f"uploads/{file_name}"

        # Upload audio to S3
        s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=audio_bytes)

        # Start transcription job asynchronously
        job_name = f"TranscribeJob-{file_id}"
        media_uri = f"s3://{BUCKET_NAME}/{s3_key}"
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat='mp3',
            LanguageCode='en-US',
            OutputBucketName=BUCKET_NAME
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'file_name': file_name})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({ "error": str(e) })
        }
