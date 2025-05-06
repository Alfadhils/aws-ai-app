import json
import boto3

# Initialize the S3 and Transcribe clients
s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
            
        job_code = body["job_code"]
        job_name = f"TranscribeJob-{job_code}"
        
        # Fetch the transcription job result
        response = get_transcription(job_name)
        if response["status"] != "COMPLETED":
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": response.get("error", "Transcription failed.")
                })
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "transcription": response["transcript"]
                })
            }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }

# Function to fetch the transcription result using the job name
def get_transcription(job_name):
    # Fetch the transcription job status
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    
    # Check if the transcription job is completed or failed
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        s3_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        
        # Parse the S3 URL into bucket name and key
        s3_bucket = s3_url.split('/')[3]
        s3_key = '/'.join(s3_url.split('/')[4:])
        
        # Fetch the transcription file from the S3 bucket
        transcript_response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
        transcript_data = json.loads(transcript_response['Body'].read().decode('utf-8'))
        transcript = transcript_data['results']['transcripts'][0]['transcript']
        return {"status": "COMPLETED", "transcript": transcript}
    
    elif status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
        return {"status": "FAILED", "error": "transcription job failed."}
    else:
        return {"status": "OTHER", "error": "transcription job does not exist or is not completed."}
