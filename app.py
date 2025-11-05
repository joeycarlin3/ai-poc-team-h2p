import streamlit as st
from streamlit_mic_recorder import mic_recorder
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
st.write("Record your answer and get AI-powered feedback.")

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

# Record audio
audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹️ Stop", key="recorder")

audio_file = None
if audio and "audio" in audio:
    st.audio(audio["audio"], format="audio/wav")
    audio_file = audio["audio"]

# Upload audio file
uploaded_file = st.file_uploader("📁 Or upload a .wav file instead", type=["wav"])
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
    st.info("🎙️ Waiting for audio input or file upload...")
