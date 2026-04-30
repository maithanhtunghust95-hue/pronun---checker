import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.markdown("""
<style>
.pulse-mic {
    font-size: 60px;
    text-align: center;
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0% {transform: scale(1);}
    50% {transform: scale(1.2);}
    100% {transform: scale(1);}
}
</style>
""", unsafe_allow_html=True)

st.write("### Record your voice")

audio_bytes = audio_recorder(
    text="",
    icon_name="microphone",
    icon_size="3x"
)

if audio_bytes:
    st.markdown('<div class="pulse-mic">🎤</div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="font-size:60px;text-align:center;">🎤</div>', unsafe_allow_html=True)
