import streamlit as st
import speech_recognition as sr
import tempfile

# ------------------------------
st.title("🎤 음성 파일 텍스트 변환기")
st.write("WAV 음성 파일을 업로드하면 텍스트로 변환해드려요.")

# ------------------------------
language_option = st.selectbox("음성의 언어를 선택하세요", ["한국어", "영어"])
language_code = "ko-KR" if language_option == "한국어" else "en-US"

# ------------------------------
uploaded_file = st.file_uploader("🎧 음성 파일을 업로드하세요 (WAV만 지원)", type=["wav"])

# ------------------------------
if uploaded_file is not None:
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    with sr.AudioFile(temp_audio_path) as source:
        st.info("음성을 분석 중입니다...")
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language=language_code)
            st.success("📝 인식된 텍스트:")
            st.write(f"{language_option}: {text}")   # ✅ 여기에서 언어 정보 함께 출력

        except sr.UnknownValueError:
            st.error("❌ 음성을 이해하지 못했어요.")
        except sr.RequestError as e:
            st.error(f"❌ Google API 요청 오류: {e}")
