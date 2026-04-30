import streamlit as st
import difflib
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import tempfile

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# CSS mic pulse
st.markdown("""
<style>
button {
    animation: pulse 1.2s infinite;
    border-radius: 50%;
}

@keyframes pulse {
    0% {transform: scale(1);}
    50% {transform: scale(1.15);}
    100% {transform: scale(1);}
}
</style>
""", unsafe_allow_html=True)

st.title("Pronunciation Checker")

# Your preset sentences
sentences = [
    "Rich people focus on opportunities.",
    "Poor people focus on obstacles.",
    "Rich people think big.",
    "Poor people think small.",
    "Take responsibility for your life.",
    "Your income can grow only to the extent that you do.",
    "Action is the bridge between intention and reality.",
    "Money is a result.",
    "You become what you think about.",
    "Success comes from consistent action."
]

# initialize session state
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

current_sentence = sentences[st.session_state.current_index]

st.write(f"### Sentence {st.session_state.current_index + 1}/{len(sentences)}")
st.write(f"**{current_sentence}**")

# recorder
audio_bytes = audio_recorder(
    text="",
    icon_name="microphone",
    icon_size="3x"
)

uploaded_file = st.file_uploader(
    "Or upload audio file",
    type=["mp3", "wav", "m4a"]
)

audio_source = None

if audio_bytes:
    audio_source = audio_bytes
elif uploaded_file:
    audio_source = uploaded_file.read()

if audio_source:
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
        current_sentence.lower(),
        transcript.lower()
    ).ratio()

    score = round(similarity * 100)

    st.write("## Result")
    st.write("**Transcript:**", transcript)
    st.write(f"**Score:** {score}/100")

# next button
if st.button("Next Sentence"):
    if st.session_state.current_index < len(sentences) - 1:
        st.session_state.current_index += 1
        st.rerun()
