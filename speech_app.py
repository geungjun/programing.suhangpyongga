import streamlit as st
import speech_recognition as sr
import tempfile

st.title("🎧 WAV 음성 텍스트 변환기")

# 언어 선택
lang = st.selectbox("음성의 언어를 선택하세요", ["한국어", "영어"])
lang_code = "ko-KR" if lang == "한국어" else "en-US"

# 파일 업로드
uploaded_file = st.file_uploader("WAV 파일 업로드", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    # 파일을 임시로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # 음성 인식
    recognizer = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language=lang_code)
        st.subheader("📝 인식된 텍스트")
        st.write(text)
    except sr.UnknownValueError:
        st.error("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        st.error(f"음성 인식 서비스 오류: {e}")
