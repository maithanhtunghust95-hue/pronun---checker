import streamlit as st
import difflib
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import tempfile

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Pronunciation Checker")

target = st.text_input("Enter target sentence")

st.write("### Record your voice")
audio_bytes = audio_recorder()

uploaded_file = st.file_uploader(
    "Or upload your audio",
    type=["mp3", "wav", "m4a"]
)

audio_source = None

if audio_bytes:
    audio_source = audio_bytes
elif uploaded_file:
    audio_source = uploaded_file.read()

if audio_source and target:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_source)
        temp_path = tmp_file.name

    with open(temp_path, "rb") as audio_file:
        transcript_response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    transcript = transcript_response.text

    similarity = difflib.SequenceMatcher(
        None,
        target.lower(),
        transcript.lower()
    ).ratio()

    score = round(similarity * 100)

    st.write("## Result")
    st.write("**Target:**", target)
    st.write("**Transcript:**", transcript)
    st.write(f"**Score:** {score}/100")
