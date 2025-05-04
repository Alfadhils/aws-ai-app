import streamlit as st
import requests
import base64
import tempfile
import os

# Title and description
st.title("🎤 Amazon Polly – Text to Speech")
st.markdown("""
This app lets you synthesize text to speech using **Amazon Polly**.  
Select a language and voice, enter your text, and listen to the synthesized audio.
""")

# Language and corresponding voices
voice_options = {
    "en-AU": {
        "label": "English, Australian",
        "voices": {"Olivia (Female)": "Olivia"}
    },
    "en-GB": {
        "label": "English, British",
        "voices": {
            "Emma (Female)": "Emma",
            "Amy (Female)": "Amy",
            "Brian (Male)": "Brian",
            "Arthur (Male)": "Arthur"
        }
    },
    "en-IN": {
        "label": "English, Indian",
        "voices": {"Kajal (Female)": "Kajal"}
    },
    "en-US": {
        "label": "English, US",
        "voices": {
            "Danielle (Female)": "Danielle",
            "Joanna (Female)": "Joanna",
            "Gregory (Male)": "Gregory",
            "Kevin (Male)": "Kevin"
        }
    }
}

# Select language
language_code = st.selectbox(
    "Select Language",
    options=list(voice_options.keys()),
    format_func=lambda code: voice_options[code]["label"]
)

# Select voice based on selected language
available_voices = voice_options[language_code]["voices"]
voice_label = st.selectbox("Select Voice", list(available_voices.keys()))
voice_id = available_voices[voice_label]

# Text input
text_input = st.text_area("Enter text to synthesize:", height=150)

# Generate button (disabled when text is empty)
generate_btn = st.button("Generate Speech", disabled=not text_input.strip())

if generate_btn:
    with st.spinner("Synthesizing text..."):
        payload = {
            "text": text_input,
            "language_code": language_code,
            "voice_id": voice_id,
            "engine": "neural"
        }

        api_url = f"{st.secrets['API_URL']}/polly"
        headers = {"x-api-key": st.secrets["API_KEY"]} if st.secrets["API_KEY"] else {}
        response = requests.post(api_url, json=payload, headers=headers)

        if response.ok:
            result = response.json()
            audio_base64 = result.get("audio_base64")
            audio_data = base64.b64decode(audio_base64)

            # Save and play audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(audio_data)
                audio_path = tmp_file.name

            st.audio(audio_path)
            os.remove(audio_path)
        else:
            st.error("Failed to generate speech. Please try again later.")
