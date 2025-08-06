import streamlit as st
import speech_recognition as sr
import tempfile

st.title("🎤 음성 파일 텍스트 변환기")
st.write("음성 파일(WAV/MP3)을 업로드하면 텍스트로 변환해드려요.")

# 파일 업로더
uploaded_file = st.file_uploader("음성 파일을 업로드하세요", type=["wav", "mp3"])

if uploaded_file is not None:
    recognizer = sr.Recognizer()

    # Streamlit의 UploadedFile을 tempfile로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name[-4:]) as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    # 음성 파일 열기
    with sr.AudioFile(temp_audio_path) as source:
        st.info("음성 분석 중입니다...")
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language="ko-KR")
            st.success("✅ 텍스트 인식 결과:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("❌ 음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            st.error(f"❌ Google API 요청 오류: {e}")
