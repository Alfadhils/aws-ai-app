import streamlit as st
import pandas as pd
import requests
import base64
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
from PIL import ImageFont
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

# Load labels from CSV
@st.cache_data
def load_labels():
    return pd.read_csv("AmazonRekognitionBoundingBoxLabels_v3.0.csv")["Label"].tolist()

st.title("🖼️ Amazon Rekognition – Image Object Detection")

st.markdown("""
Upload an image to detect objects using **Amazon Rekognition**. This tool identifies objects, scenes, and concepts in your image based on Labels you provide and visualizes them with bounding boxes.
""")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Multiselect labels
valid_labels = load_labels()
selected_labels = st.multiselect("Select expected labels (for validation)", valid_labels)

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded image preview", use_container_width=True)

# Submit
if uploaded_file and selected_labels and st.button("Analyze Image"):
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode()

    # Send to API Gateway
    api_url = "https://nucadh7rm4.execute-api.ap-southeast-1.amazonaws.com/prod/rekognition"
    payload = {
        "image_base64": image_base64,
        "selected_labels": selected_labels
    }
    headers = {"x-api-key": api_key}

    with st.spinner("Analyzing Image..."):
        response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
    else:
        result = response.json()
        labels = result.get("labels", [])

        image = Image.open(BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image).convert("RGB")
        draw = ImageDraw.Draw(image)
        width, height = image.size

        for label in labels:
            for instance in label.get("Instances", []):
                box = instance["BoundingBox"]
                left = box["Left"] * width
                top = box["Top"] * height
                w = box["Width"] * width
                h = box["Height"] * height
                draw.rectangle([left, top, left + w, top + h], outline="black", width=4)
                draw.rectangle([left+1, top+1, left + w - 1, top + h - 1], outline="white", width=2)
                font_size = 25  # Adjust font size as needed
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    font = None  # Fallback if the font is not available
                draw.text((left, top), label["Name"], fill="white", stroke_width=1, stroke_fill="black", font=font)
                

        st.image(image, caption="Detected objects with bounding boxes", use_container_width=True)
        
        st.subheader("Detected Labels")
        for label in labels:
            st.write(f"**{label['Name']}**: {label['Confidence']:.2f}%")

