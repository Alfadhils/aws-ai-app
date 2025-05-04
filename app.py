import streamlit as st
from PIL import Image

st.set_page_config(page_title="AWS AI Services Demo", layout="centered")

aws_logo = Image.open("assets/aws-logo-scaled.jpg")

home = st.Page("home.py", title="Home", icon=":material/home:")
rekognition = st.Page("AI Services/rekognition.py", title="🖼️ Amazon Rekognition")
textract = st.Page("AI Services/textract.py", title="📄 Amazon Textract")
polly = st.Page("AI Services/polly.py", title="🎤 Amazon Polly")
transcribe = st.Page("AI Services/transcribe.py", title="🎙️ Amazon Transcribe")
comprehend = st.Page("AI Services/comprehend.py", title="🧠 Amazon Comprehend")

pg = st.navigation(
        {
            "Home": [home],
            "AI Services": [rekognition, textract, polly, transcribe, comprehend],
        }
    )

st.sidebar.markdown("**API Settings :**")
st.sidebar.success("✅ Public API Key Provided!")
st.sidebar.markdown("----")

# Footer Section
st.sidebar.markdown("**Author:** Fadhil Umar Al Farouq")
st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/fadhil-u-bb7065140/)")
st.sidebar.markdown("[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Alfadhils)")
st.sidebar.markdown("[![Website](https://img.shields.io/badge/Website-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)](https://alfadhils.github.io)")

pg.run()
