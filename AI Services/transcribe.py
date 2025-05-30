import streamlit as st
import requests
import base64
from audio_recorder_streamlit import audio_recorder

st.title("🎙️ Amazon Transcribe – Audio Transcription")

st.markdown("""
This tool allows you to record audio, submit it for transcription, and retrieve the transcription result. 
Once you record and submit the audio, a transcription job is initiated, and you can check the status using the job code.
""")

# Function to upload audio to Transcribe service
def transcribe_audio(audio_bytes):
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    # Send to Transcribe API endpoint
    api_url = f"{st.secrets['API_URL']}/transcribe"
    payload = {"audio_base64": audio_base64}
    headers = {"x-api-key": st.secrets["API_KEY"]} if st.secrets["API_KEY"] else {}
    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.ok:
        response_data = response.json()
        
        # Return job code from response
        file_name = response_data.get("file_name")
        if file_name and file_name.endswith(".mp3"):
            job_code = file_name[:-4]
        st.success(f"Transcription job initiated successfully! **Please store the job code as it will not be displayed again.** Job code: {job_code}")
        return job_code
    else:
        st.error("Failed to initiate transcription job.")
        return None

# Function to check the status of the transcription job
def check_job_status(job_code):
    
    # Send to Transcribe Fetch API endpoint
    api_url = f"{st.secrets['API_URL']}/transcribe"
    payload = {"job_code": job_code}
    headers = {"x-api-key": st.secrets["API_KEY"]} if st.secrets["API_KEY"] else {}
    response = requests.get(api_url, json=payload, headers=headers)
    
    if response.ok:
        job_status = response.json()
        
        # Return transcription result from response
        transcription = job_status.get("transcription", "No transcription found.")
        return transcription
    else:
        job_status = response.json()
        st.error(job_status.get("error", "Failed to fetch transcription status."))
        return None

# Audio Recording Section
st.subheader("Step 1: Record Your Audio")

audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    # Button to submit audio for transcription
    if st.button("Submit Audio for Transcription"):
        job_code = transcribe_audio(audio_bytes)

# Check Job Status Section
st.subheader("Step 2: Check Job Status")

job_code_input = st.text_input("Enter Transcription Job Code")
if job_code_input:
    if st.button("Check Status"):
        # Retrieve transcription result using job code
        transcription = check_job_status(job_code_input)
        if transcription:
            st.markdown(f"### Transcription Result: \n\n{transcription}")
