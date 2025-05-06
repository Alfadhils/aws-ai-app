import streamlit as st
import pandas as pd
import requests
import base64
from PIL import Image, ImageDraw
from io import BytesIO

# Load labels from CSV
@st.cache_data
def load_labels():
    return pd.read_csv("assets/AmazonRekognitionBoundingBoxLabels_v3.0.csv")["Label"].tolist()

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
    # Show preview
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image preview", use_container_width=True)
    
    # Submit button
    if st.button("Analyze Image"):
        with st.spinner("Analyzing Image..."):
            # Encode image to base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Send to rekognition API endpoint
            api_url = f"{st.secrets['API_URL']}/rekognition"
            headers = {"x-api-key": st.secrets["API_KEY"]} if st.secrets["API_KEY"] else {}
            payload = {"image_base64": image_base64, "selected_labels": selected_labels}
            response = requests.post(api_url, json=payload, headers=headers)
            
            if response.ok:
                result = response.json()
                labels = result.get("labels", [])

                draw_image = image.copy()
                draw = ImageDraw.Draw(draw_image)
                width, height = draw_image.size

                # Draw bounding boxes and labels
                for label in labels:
                    for instance in label.get("Instances", []):
                        box = instance["BoundingBox"]
                        x0 = box["Left"] * width
                        y0 = box["Top"] * height
                        x1 = x0 + box["Width"] * width
                        y1 = y0 + box["Height"] * height
                        
                        draw.rectangle([x0, y0, x1, y1], outline="black", width=3)
                        draw.rectangle([x0+1, y0+1, x1-1, y1-1], outline="white", width=1)
                        draw.text((x0 + 2, y0 - 12), label["Name"], fill="white", stroke_width=1, stroke_fill="black")
                        
                # Show image with boxes
                st.image(draw_image, caption="Detected objects with bounding boxes", use_container_width=True)
                
                # Display detected labels
                st.subheader("Detected Labels")
                for label in labels:
                    st.write(f"• **{label['Name']}** (Confidence: {label['Confidence']:.2f}%)")
                    
            else:
                st.error("Error analyzing image. Please try again.")

