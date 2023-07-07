import json
import streamlit as st
import soundfile as sf
import openai
from audiorecorder import audiorecorder
import whisper
from teacherAgent import askTeacher

with open("credentials.json", "r") as f:
    api = json.load(f)
    key = api["openai"]

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Recording...")



@st.cache_data
def load_model():
    model = whisper.load_model("base")
    return model

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.tobytes())
    
    # To save audio to a file:
    wav_file = open("audio.mp3", "wb")
    wav_file.write(audio.tobytes())
    
    def transcribe(file):
        result = model.transcribe(file)
        return result["text"]

if st.button('Correct the sentences'):

    # Cargar el archivo de audio
    audio_file = open("audio.mp3", "rb")
    # Leer el contenido del archivo de audio
    audio_content = audio_file.read()
    # Definir el prompt
    model = load_model()

    with st.spinner("waiting"):
        transcription = transcribe("audio.mp3")
        result = askTeacher(transcription)
        st.write(result)
        print(result)
        with st.chat_message("result"):
            st.write(transcription)
            st.write("Hello 👋, " + result)











