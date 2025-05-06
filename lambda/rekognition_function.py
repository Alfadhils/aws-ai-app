import json
import boto3
import base64

# Initialize the Rekognition client
rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
            
        image_base64 = body["image_base64"]
        image_bytes = base64.b64decode(image_base64)
        selected_labels = set(label.lower() for label in body.get("selected_labels", []))

        # Use Rekognition to detect labels in the image
        response = rekognition.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=50,
            MinConfidence=50
        )

        # Filter labels based on selected labels
        filtered_labels_info = []
        for label in response['Labels']:
            if label['Name'].lower() in selected_labels:
                label_data = {
                    "Name": label['Name'],
                    "Confidence": label['Confidence'],
                    "Instances": []
                }

                for instance in label.get("Instances", []):
                    box = instance.get("BoundingBox", {})
                    label_data["Instances"].append({
                        "BoundingBox": box,
                        "Confidence": instance.get("Confidence")
                    })

                filtered_labels_info.append(label_data)

        return {
            'statusCode': 200,
            'body': json.dumps({ "labels": filtered_labels_info })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({ "error": str(e) })
        }
