import streamlit as st

import whisper

model = whisper.load_model("base")

st.text("Whisper model loaded")