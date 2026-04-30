import streamlit as st
import difflib
from openai import OpenAI
import tempfile

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Pronunciation Checker")

target = st.text_input("Enter target sentence")

uploaded_file = st.file_uploader(
    "Upload your audio",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file and target:
    # save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    # transcribe audio with Whisper
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
