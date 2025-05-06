import streamlit as st
import requests

st.title("🧠 Amazon Comprehend – Sentiment & Entity Detection")

st.markdown("""
Enter a sentence or paragraph below to analyze its **sentiment** and **named entities**.
""")

# Text input
input_text = st.text_area("Input Text", height=150)

# Analyze button
analyze_button = st.button("Analyze", disabled=not input_text.strip())

if analyze_button:
    with st.spinner("Analyzing text..."):
        # Send to comprehend API endpoint
        api_url = f"{st.secrets['API_URL']}/comprehend"
        headers = {"x-api-key": st.secrets["API_KEY"]} if st.secrets["API_KEY"] else {}
        payload = {"text": input_text}
        response = requests.post(api_url, json=payload, headers=headers)

        if response.ok:
            result = response.json()

            # Display sentiment
            st.subheader("Sentiment Analysis")
            st.markdown(f"**Sentiment:** `{result.get('sentiment', 'Unknown')}`")
            st.markdown("**Confidence Scores:**")
            for k, v in result.get("sentiment_score", {}).items():
                st.write(f"- {k}: {v:.2f}")

            # Display entities
            st.subheader("Detected Entities")
            entities = result.get("entities", [])
            if entities:
                for ent in entities:
                    st.markdown(
                        f"- **{ent.get('Text')}** — *{ent.get('Type')}* (Score: {ent.get('Score'):.2f})"
                    )
            else:
                st.info("No entities detected.")
                
        else:
            st.error("Failed to analyze text. Please try again.")

