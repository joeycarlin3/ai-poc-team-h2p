import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import whisper
import tempfile
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("🚨 No API key found! Make sure GOOGLE_API_KEY is in your .env file.")
else:
    genai.configure(api_key=API_KEY)

st.title("🎤 AI Interview Practice Tool")
st.write("Upload your recorded answer as a .wav file and get AI-powered feedback.")

# Dropdown for questions
questions = [
    "Tell me about yourself.",
    "Why do you want this role?",
    "What are your strengths?",
    "Tell me about a challenge you faced.",
]
question = st.selectbox("Choose an interview question:", questions)
st.subheader("Interview Question:")
st.write(question)

# Upload audio file
st.subheader("📁 Upload your answer")
st.markdown("""
To use this tool:
1. Record your answer using any voice recorder app on your phone or computer.
2. Save the recording as a `.wav` file.
3. Upload the file below to get transcription and feedback.
""")

uploaded_file = st.file_uploader("Upload a .wav file", type=["wav"])

audio_file = None
if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    audio_file = open(tmp_path, "rb").read()

# Transcribe and analyze
if audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file)
        tmp_path = tmp_file.name

    try:
        st.write("📥 Audio file saved at:", tmp_path)
        whisper_model = whisper.load_model("base")
        st.write("🔍 Whisper model loaded")
        result = whisper_model.transcribe(tmp_path)
        transcription = result["text"]
        st.subheader("📝 Transcription:")
        st.write(transcription)
    except Exception as e:
        st.error(f"Transcription error: {e}")
        transcription = None

    if transcription:
        with st.spinner("🤖 Getting AI feedback..."):
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            prompt = f"""
            You are an interview coach. The question was: "{question}"
            Here is the candidate's transcribed answer: "{transcription}"

            Evaluate the answer and give feedback on:
            - Clarity & structure
            - Confidence & tone
            - Strengths
            - Improvements
            - Suggested better answer

            End with a score out of 10.
            """
            try:
                response = model.generate_content(prompt)
                st.subheader("✅ AI Feedback:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Gemini error: {e}")
else:
    st.info("📂 Please upload a .wav file to continue.")
