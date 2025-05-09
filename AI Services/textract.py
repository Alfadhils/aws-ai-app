import streamlit as st
from PIL import Image, ImageDraw
from pdf2image import convert_from_bytes
import requests
import base64
import io

st.title("📄 Amazon Textract – Invoice Text Extraction")

st.markdown("""
Upload an image or scanned PDF of an invoice. This tool uses **Amazon Textract** to detect raw texts and visualize them with bounding boxes.
""")

# Upload document
uploaded_file = st.file_uploader("Upload Invoice Image or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    # Show preview
    if uploaded_file.type == "application/pdf":
        images = convert_from_bytes(uploaded_file.read(), first_page=1, last_page=1)
        image = images[0]
        st.image(image, caption="First Page of Uploaded PDF", use_container_width=True)
    else:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Invoice", use_container_width=True)

    # Submit button
    if st.button("Extract Text"):
        with st.spinner("Analyzing Document..."):
            # Encode image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Send to textract API endpoint
            api_url = f"{st.secrets['API_URL']}/textract"
            headers = {"x-api-key": st.secrets["API_KEY"]} if st.secrets["API_KEY"] else {}
            payload = {"image_base64": image_base64}
            response = requests.post(api_url, json=payload, headers=headers)

            if response.ok:
                result = response.json()
                text_blocks = result.get("text_blocks", [])

                draw_image = image.copy()
                draw = ImageDraw.Draw(draw_image)
                width, height = draw_image.size

                # Draw bounding boxes and labels
                for block in text_blocks:
                    box = block["BoundingBox"]
                    text = block["Text"]
                    conf = block["Confidence"]

                    x0 = box["Left"] * width
                    y0 = box["Top"] * height
                    x1 = x0 + box["Width"] * width
                    y1 = y0 + box["Height"] * height

                    draw.rectangle([x0, y0, x1, y1], outline="black", width=3)
                    draw.rectangle([x0+1, y0+1, x1-1, y1-1], outline="white", width=1)
                    
                    draw.text((x0 + 2, y0 - 12), text, fill="white", stroke_width=1, stroke_fill="black")

                # Show image with boxes
                st.image(draw_image, caption="Detected Text with Bounding Boxes", use_container_width=True)

                # Show detected texts
                st.subheader("Detected Texts")
                for block in text_blocks:
                    st.write(f"• **{block['Text']}** (Confidence: {block['Confidence']:.2f}%)")
                    
            else:
                st.error("Error analyzing document. Please try again.")
