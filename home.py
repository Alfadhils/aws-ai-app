import streamlit as st

# Title
st.title("🤖 AWS AI Services Showcase")

# Author and intro
st.write("Built by **Fadhil Umar Al Farouq**")
st.write("AI & Cloud Specialists")

st.write("---")

# Solutions Overview
st.subheader("Solutions Overview")
st.write("""
AWS AI Services provide **ready-to-use AI capabilities** that eliminate the need for building or training machine learning models from scratch. With just a simple **API call**, you can access advanced features like *image and video analysis*, *text extraction*, *speech-to-text conversion*, and *sentiment analysis*. 

These services enable developers to quickly integrate AI-powered functionality into their applications without requiring deep expertise in machine learning or managing complex infrastructure.

As part of the AWS ML/AI stack, these services offer the highest level of abstraction, making them the easiest and most managed way to add AI to your solutions.
""")

st.image("assets/aws_ml_stack.png", caption="AWS ML/AI Stacks")

# Featured AWS AI Services
st.subheader("🌟 Featured AWS AI Services:")
st.write("- 🖼️ Image Object Detection (Amazon Rekognition)")
st.write("- 📄 Invoice Text Extraction (Amazon Textract)")
st.write("- 🎤 Text to Speech (Amazon Polly)")
st.write("- 🎙️ Audio Transcription (Amazon Transcribe)")
st.write("- 🧠 Sentiment & Entity Detection (Amazon Comprehend)")

st.info("👈 Use the sidebar to navigate between services and try each AI feature live!")

# Architecture Overview
st.subheader("Architecture Overview")

st.write(
    "In this showcase application, an API Gateway is implemented to route requests to the appropriate AWS AI Service. "
    "This architecture simplifies the integration process and ensures that each service is accessed efficiently."
)

st.image("assets/ai-services-architecture.png", caption="AWS AI Services Architecture")