import json
import boto3
import base64

# Initialize the Textract client
textract = boto3.client('textract')

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)

        image_base64 = body["image_base64"]
        image_bytes = base64.b64decode(image_base64)

        # Use Textract to detect raw document text
        response = textract.detect_document_text(
            Document={'Bytes': image_bytes}
        )

        # Collect LINE blocks
        blocks = response.get("Blocks", [])
        results = []
        for block in blocks:
            if block["BlockType"] in ["LINE"]:
                results.append({
                    "Text": block["Text"],
                    "Confidence": block["Confidence"],
                    "BoundingBox": block["Geometry"]["BoundingBox"],
                    "BlockType": block["BlockType"]
                })

        return {
            "statusCode": 200,
            "body": json.dumps({"text_blocks": results})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
