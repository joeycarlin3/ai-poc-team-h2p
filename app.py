import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("🚨 No API key found! Make sure GEMINI_API_KEY is in your .env file.")
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

if st.button("Get AI Feedback"):
    if not audio_file:
        st.warning("Please record an answer first!")
    else:
        with st.spinner("🎧 Transcribing & analyzing your answer..."):

            # Prepare audio for Gemini
            encoded_audio = base64.b64encode(audio_file).decode("utf-8")
            gemini_audio = {
                "mime_type": "audio/wav",
                "data": encoded_audio,
            }

            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            You are an interview coach. The question was: "{question}"
            Evaluate the candidate's answer. Give feedback on:

            - Clarity & structure
            - Confidence & tone
            - Strengths
            - Improvements
            - Suggested better answer

            End with a score out of 10.
            """

            try:
                response = model.generate_content([prompt, gemini_audio])
                st.success("✅ Feedback Received")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
