import streamlit as st
import difflib
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import tempfile
import random

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎤 Công cụ luyện phát âm")

# Danh sách câu
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

compliments = [
    "🌸 BẠN LÀM TỐT LẮM!",
    "🌺 GIỎI GHÊ TA!",
    "🌷 PHÁT ÂM ĐỈNH CHÓP ĐÓ!",
    "💐 TIẾN BỘ RÕ LUÔN!"
]

# State
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "scores" not in st.session_state:
    st.session_state.scores = []

current_sentence = sentences[st.session_state.current_index]

# UI
st.markdown("### Hướng dẫn")
st.write("1. Bấm micro để ghi âm.")
st.write("2. Đọc to câu bên dưới.")
st.write("3. Xem điểm và chuyển câu tiếp theo.")

st.write("---")

st.write(f"### Câu {st.session_state.current_index + 1}/{len(sentences)}")

st.markdown(
    f"<h1 style='text-align:center; font-weight:bold;'>{current_sentence}</h1>",
    unsafe_allow_html=True
)

# Recorder (KEY QUAN TRỌNG để tránh bug)
audio_bytes = audio_recorder(
    text="",
    icon_name="microphone",
    icon_size="3x",
    key=f"recorder_{st.session_state.current_index}"
)

uploaded_file = st.file_uploader(
    "Hoặc tải file audio",
    type=["mp3", "wav", "m4a"]
)

audio_source = None
if audio_bytes:
    audio_source = audio_bytes
elif uploaded_file:
    audio_source = uploaded_file.read()

# Xử lý
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

    # lưu score
    if len(st.session_state.scores) <= st.session_state.current_index:
        st.session_state.scores.append(score)
    else:
        st.session_state.scores[st.session_state.current_index] = score

    # hiển thị
    st.write("## Kết quả")
    st.write("**Máy nghe được:**", transcript)
    st.write(f"**Điểm phát âm:** {score}/100")

    # feedback
    if score >= 80:
        st.markdown(
            f"<h2 style='color:red; text-align:center;'>{random.choice(compliments)}</h2>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<h2 style='color:orange; text-align:center;'>💪 TIẾP TỤC CỐ GẮNG NHA, THÊM 1 LẦN NỮA ĐI!</h2>",
            unsafe_allow_html=True
        )

# Next button
if st.button("➡️ Câu tiếp theo"):
    if st.session_state.current_index < len(sentences) - 1:
        st.session_state.current_index += 1
        st.rerun()

# 🎯 HIỆN KẾT QUẢ CUỐI
# 🎯 HIỆN KẾT QUẢ CUỐI
if (
    st.session_state.current_index == len(sentences) - 1
    and len(st.session_state.scores) == len(sentences)
):
    avg = round(sum(st.session_state.scores) / len(st.session_state.scores))

    st.write("---")
    st.markdown(
        "<h1 style='text-align:center;'>🎉 HOÀN THÀNH BÀI LUYỆN 🎉</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h2 style='text-align:center; color:blue;'>Điểm trung bình: {avg}/100</h2>",
        unsafe_allow_html=True
    )

    # feedback cuối bài
    if avg >= 80:
        st.markdown(
            "<h2 style='color:red; text-align:center;'>🌸 BẠN ĐANG TIẾN BỘ RẤT TỐT!</h2>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<h2 style='color:orange; text-align:center;'>💪 LUYỆN THÊM CHÚT NỮA LÀ SẼ RẤT ỔN!</h2>",
            unsafe_allow_html=True
        )

    # bảng chi tiết
    st.write("### 📊 Chi tiết từng câu")

    data = {
        "Câu": [f"Câu {i+1}" for i in range(len(sentences))],
        "Nội dung": sentences,
        "Điểm": st.session_state.scores
    }

    st.table(data)
