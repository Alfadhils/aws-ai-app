import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

st.title("🧠 Amazon Comprehend – Sentiment & Entity Detection")

# Overview Section
st.markdown("Enter a sentence or paragraph below to analyze its **sentiment** and **named entities**.")

# Text input
input_text = st.text_area("Input Text", height=150)

# Disable analyze button if input is empty
analyze_button = st.button("Analyze", disabled=not input_text.strip())

# Run only when button clicked
if analyze_button:
    with st.spinner("Analyzing text..."):
        try:
            api_url = "https://nucadh7rm4.execute-api.ap-southeast-1.amazonaws.com/prod/comprehend"
            headers = {"x-api-key": api_key}
            payload = {"text": input_text}
            response = requests.post(api_url, json=payload, headers=headers)

            if response.ok:
                data = response.json()

                # Display sentiment
                st.subheader("🔍 Sentiment Analysis")
                st.markdown(f"**Sentiment:** `{data.get('sentiment', 'Unknown')}`")
                st.markdown("**Confidence Scores:**")
                for k, v in data.get("sentiment_score", {}).items():
                    st.write(f"- {k}: {v:.2f}")

                # Display entities
                st.subheader("📌 Detected Entities")
                entities = data.get("entities", [])
                if entities:
                    for ent in entities:
                        st.markdown(
                            f"- **{ent.get('Text')}** — *{ent.get('Type')}* (Score: {ent.get('Score'):.2f})"
                        )
                else:
                    st.info("No entities detected.")
            else:
                st.error("Failed to analyze text. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
