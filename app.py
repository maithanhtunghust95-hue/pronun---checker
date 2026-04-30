import streamlit as st
import difflib

st.title("Pronunciation Checker")

target = st.text_input("Enter target sentence")

uploaded_file = st.file_uploader(
    "Upload audio",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file and target:
    transcript = st.text_input(
        "Transcript",
        value=target
    )

    similarity = difflib.SequenceMatcher(
        None,
        target.lower(),
        transcript.lower()
    ).ratio()

    score = round(similarity * 100)

    st.write("### Result")
    st.write("Score:", score)
