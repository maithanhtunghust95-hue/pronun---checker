import streamlit as st
import difflib
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import tempfile
import random

# Kết nối OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Tiêu đề app
st.title("🎤 Công cụ luyện phát âm")

# Danh sách câu luyện tập
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

# Lời khen
compliments = [
    "🌸 BẠN LÀM TỐT LẮM!",
    "🌺 GIỎI GHÊ TA!",
    "🌷 PHÁT ÂM ĐỈNH CHÓP ĐÓ!",
    "💐 TIẾN BỘ RÕ LUÔN!"
]

# Lưu trạng thái câu hiện tại
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

current_sentence = sentences[st.session_state.current_index]

# Hướng dẫn
st.markdown("### Hướng dẫn")
st.write("1. Bấm vào biểu tượng micro để ghi âm.")
st.write("2. Đọc to và rõ câu tiếng Anh bên dưới.")
st.write("3. Xem điểm phát âm.")
st.write("4. Bấm 'Câu tiếp theo' để chuyển câu mới.")

st.write("---")

# Hiển thị số câu
st.write(f"### Câu {st.session_state.current_index + 1}/{len(sentences)}")

# Hiển thị câu target thật to
st.markdown(
    f"<h1 style='text-align:center; font-weight:bold;'>{current_sentence}</h1>",
    unsafe_allow_html=True
)

st.write("### 🎙️ Bấm micro để ghi âm")

# Ghi âm
audio_bytes = audio_recorder(
    text="",
    icon_name="microphone",
    icon_size="3x"
)

# Upload file backup
uploaded_file = st.file_uploader(
    "Hoặc tải file audio lên",
    type=["mp3", "wav", "m4a"]
)

audio_source = None

if audio_bytes:
    audio_source = audio_bytes
elif uploaded_file:
    audio_source = uploaded_file.read()

# Xử lý audio
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

    # Hiển thị kết quả
    st.write("## Kết quả")
    st.write("**Máy nghe được:**", transcript)
    st.write(f"**Điểm phát âm:** {score}/100")

    # Feedback theo score
    if score >= 80:
        message = random.choice(compliments)

        st.markdown(
            f"<h2 style='color:red; text-align:center;'>{message}</h2>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<h2 style='color:orange; text-align:center;'>💪 TIẾP TỤC CỐ GẮNG NHA, THÊM 1 LẦN NỮA ĐI!</h2>",
            unsafe_allow_html=True
        )

# Nút chuyển câu
if st.button("➡️ Câu tiếp theo"):
    if st.session_state.current_index < len(sentences) - 1:
        st.session_state.current_index += 1
        st.rerun()
