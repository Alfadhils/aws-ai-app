# AWS AI Showcase 🚀

A Streamlit web app demonstrating the practical use cases and capabilities of **AWS AI Services**. With simple inputs, users can interact with powerful AI features like image recognition, text extraction, text-to-speech, audio transcription, and sentiment analysis — all powered by AWS.

🌐 **Live App:** [aws-ai-app.streamlit.app](https://aws-ai-app.streamlit.app/)  
📦 **GitHub Repo:** [github.com/Alfadhils/aws-ai-app](https://github.com/Alfadhils/aws-ai-app/tree/main)

---

## 🔍 Overview

AWS AI Services provide pre-built, ready-to-use machine learning features accessible via API — no ML experience required. This application showcases how developers can integrate these services into their own projects quickly and effectively.

This app serves both as:
- A **learning tool** for those new to AWS AI
- A **demonstration** for stakeholders or developers looking to adopt AI solutions with minimal overhead

---

## 🧠 Featured AI Services

| Feature | AWS Service | Description |
|--------|-------------|-------------|
| 🖼️ Image Object Detection | Amazon Rekognition | Detects objects, scenes, and concepts in an image with bounding boxes and confidence scores |
| 📄 Invoice Text Extraction | Amazon Textract | Extracts raw text and data from invoices (image or PDF) |
| 🗣️ Text to Speech | Amazon Polly | Converts text into lifelike speech audio |
| 🎙️ Audio Transcription | Amazon Transcribe | Transcribes spoken audio from microphone input |
| 💬 Sentiment & Entity Detection | Amazon Comprehend | Analyzes sentiment and detects entities from input text |

---

## 🏗️ Architecture

- **Frontend**: Streamlit web app
- **Backend Services**: AWS AI Services accessed through lambda functions controlled by API Gateway
- **Authorization**: Public API Key with built-in rate limiting
- **Integration Flow**: Simple REST endpoints map to the respective lambda functions for each AWS AI Services

---

## ▶️ Getting Started

1. Clone the repository:

```bash
git clone https://github.com/Alfadhils/aws-ai-app.git
cd aws-ai-app
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3. Create Lambda functions for the backend (use AWS Console or AWS CLI/SDK). Code is available under `/lambda`.

4. Configure REST API Gateway.

5. Integrate each method with corresponding Lambda functions and enable CORS.

6. Create an API Key and Usage Plan for public access.

7. Associate the API Key with each method.

8. Deploy the API Gateway to the `prod` stage.

9. Create a `.streamlit/secrets.toml` and add the environment variables.
For local development, use `.env` with `python-dotenv`.
```bash
API_KEY="YOUR-API-KEY-HERE"
API_URL="https://12345678.execute-api.ap-southeast-1.amazonaws.com/prod"
```

10. Run the app locally:
```bash
streamlit run app.py
```

11. Log in with GitHub on the Streamlit cloud website.

12. Deploy the app and add your secrets in the "Advanced Settings".

13. Open the deployed app using the provided URL.

## 📄 License
This project is open source and available under the MIT License.

## 📬 Contact
For any inquiries or feedback, please contact Fadhil Umar [here](mailto:fadhilumar.af@gmail.com).

