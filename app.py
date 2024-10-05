import json
import streamlit as st
import soundfile as sf
import openai
from audiorecorder import audiorecorder
import whisper
from teacherAgent import askTeacher
from io import BytesIO
from pydub import AudioSegment
from getMenuSting import getMenu

# Load API key
with open("credentials.json", "r") as f:
    api = json.load(f)
    key = api["openai"]

st.title("Audio Recorder")
st.text(getMenu())

audio = audiorecorder("Click to record", "Recording...")

# Initialize message history (stored in Streamlit session state to maintain between interactions)
if "message_history" not in st.session_state:
    st.session_state.message_history = []

@st.cache_data
def load_model():
    model = whisper.load_model("base")
    return model

# Handle audio recording
if isinstance(audio, AudioSegment):
    # Convert AudioSegment to byte stream
    audio_bytes_io = BytesIO()
    audio.export(audio_bytes_io, format="mp3")
    audio_bytes = audio_bytes_io.getvalue()

    # Play the audio in the frontend
    st.audio(audio_bytes)

    # Save the audio to an mp3 file
    with open("audio.mp3", "wb") as wav_file:
        wav_file.write(audio_bytes)

    # Transcription function
    def transcribe(file):
        model = load_model()
        result = model.transcribe(file, language="en")
        return result["text"]

    # Button to correct the transcription
    if st.button('Correct the sentences'):
        with st.spinner("Transcribing and correcting..."):
            # Transcribe the saved mp3 file
            transcription = transcribe("audio.mp3")
            
            # Append the transcription to the message history as a new HumanMessage
            st.session_state.message_history.append(f"User: {transcription}")
            
            # Get the correction from the teacherAgent with the updated history
            result = askTeacher(transcription)
            # If you want to handle the possibility of an empty JSON response
            try:
                # Convert the response string to a JSON object (Python dictionary)
                json_object = json.loads(result)
            except json.JSONDecodeError:
                # Handle the case where the response is not valid JSON
                json_object = {"items": []}

            # Now json_object is a Python dictionary representing the JSON data
            print(json_object)
            st.session_state.message_history.append(f"Agent: {result}")

            # Display results
            st.write("Transcription: ", transcription)
            st.write("Correction: ", result)

# Display the message history
st.subheader("Conversation History")
for message in st.session_state.message_history:
    st.write(message)
else:
    st.write("Please record some audio first.")


# [{agent:"text1","user":"text"}, {agent: "text2","user":"text"}]