import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import whisper
import tempfile
import os
from io import BytesIO

# --- Configuration and Initialization ---

# 1. Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Configure Gemini
if not API_KEY:
    st.error("🚨 No API key found! Make sure GOOGLE_API_KEY is in your .env file.")
else:
    # This configures the client to use the API key
    genai.configure(api_key=API_KEY)

# 3. Load Whisper Model (Cached for performance)
# Caching the model is crucial to prevent reloading on every Streamlit interaction (button press, input change)
@st.cache_resource
def load_whisper_model():
    # 'base' model is a good balance of speed and accuracy. 
    with st.spinner("Loading AI Transcription Model..."):
        return whisper.load_model("base")

# --- Streamlit UI ---

st.title("🎤 AI Interview Practice Tool")
st.markdown("Upload your recorded answer (WAV, MP3, or M4A) and get AI-powered feedback.")

# Dropdown for questions
questions = [
    "Tell me about yourself.",
    "Why do you want this role?",
    "What are your strengths?",
    "Tell me about a challenge you faced.",
    "Where do you see yourself in 5 years?",
]
question = st.selectbox("Choose an interview question:", questions)

st.divider()

# Upload audio file
st.subheader("1. Upload Your Recorded Answer")
st.info("Ensure you have installed FFmpeg (`sudo apt-get install ffmpeg`) in Codespaces for audio processing.")

uploaded_file = st.file_uploader("Upload an audio file (WAV, MP3, M4A)", type=["wav", "mp3", "m4a"])

if uploaded_file:
    # Read and display the audio in the browser
    audio_data = uploaded_file.read()
    st.audio(audio_data, format=uploaded_file.type)

    # Use a session state variable to store the transcription result
    if 'transcription_result' not in st.session_state:
        st.session_state.transcription_result = None
    
    # 2. Analyze Button
    if st.button("Analyze Answer", type="primary"):
        st.session_state.transcription_result = None
        tmp_path = None
        
        # Determine which Gemini model to use
        gemini_model_name = "gemini-2.5-flash"
        
        try:
            # --- Transcription Phase ---
            with st.spinner("🎧 Step 1/2: Transcribing audio... (This may take a moment)"):
                
                # Create a temporary file path. Whisper requires a file path.
                suffix = os.path.splitext(uploaded_file.name)[1] or ".wav"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    # Write the content from the uploaded file buffer to the temporary file
                    tmp_file.write(audio_data)
                    tmp_path = tmp_file.name
                
                # Load and run the Whisper model
                whisper_model = load_whisper_model()
                result = whisper_model.transcribe(tmp_path) 
                transcription = result["text"]
            
            st.success("Transcription Complete!")
            
            # --- Feedback Phase ---
            with st.spinner(f"🤖 Step 2/2: Getting AI feedback using {gemini_model_name}..."):
                
                model = genai.GenerativeModel(gemini_model_name)
                
                prompt = f"""
                You are an expert, constructive interview coach. 
                
                The official interview question was: "{question}"
                The Candidate's Answer (Transcribed): "{transcription}"

                Provide structured feedback on the candidate's answer based on the following criteria:
                
                1. **Executive Summary**: A concise 1-sentence summary of overall performance.
                2. **Clarity & Structure (Focus)**: Evaluate if the answer was well-organized, easy to follow, and addressed the prompt directly. Suggest specific ways to improve the structure (e.g., using the STAR method).
                3. **Content Depth & Relevance**: Assess if the details provided were strong, relevant to the question, and demonstrated appropriate skills/experience.
                4. **Tone & Confidence**: Based on the transcription's wording, evaluate the perceived confidence and professional tone.
                5. **Suggested Better Answer**: Provide a concise, model response that incorporates all necessary improvements.
                
                End with a score on a separate line: Score: X/10
                """
                
                response = model.generate_content(prompt)
                
                # Store results in session state
                st.session_state.transcription_result = {
                    "transcription": transcription,
                    "feedback": response.text
                }
                
                # Rerun to display the stored results
                st.rerun()

        except Exception as e:
            # Check for the specific 404 error and attempt fallback
            if "404 models/gemini-2.5-flash is not found" in str(e):
                gemini_model_name = "gemini-pro"
                st.warning(f"⚠️ Failed to load 'gemini-1.5-flash'. Falling back to {gemini_model_name}...")
                
                try:
                    # Retry with the fallback model
                    with st.spinner(f"🤖 Retrying with {gemini_model_name}..."):
                        model = genai.GenerativeModel(gemini_model_name)
                        response = model.generate_content(prompt)
                        st.session_state.transcription_result = {
                            "transcription": transcription,
                            "feedback": f"**Note: Used fallback model {gemini_model_name}**\n\n" + response.text
                        }
                        st.rerun()
                except Exception as fallback_e:
                    st.error(f"Fallback model failed: {fallback_e}")
            else:
                st.error(f"An error occurred during processing: {e}")
        
        finally:
            # Cleanup: Always delete the temporary file after processing
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

# --- Display Results ---

if st.session_state.get('transcription_result'):
    result = st.session_state.transcription_result
    
    # Transcription Section
    st.subheader("📝 Transcription")
    with st.expander("Click to view the full transcription"):
        st.markdown(result['transcription'])

    # Feedback Section
    st.subheader("✅ Coach's Feedback")
    st.markdown(result['feedback'])

else:
    st.info("👆 Upload a file and click 'Analyze Answer' to see results.")