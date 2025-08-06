import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import tempfile
import os

# 타이틀
st.title("🎙️ WAV 음성 파일 텍스트 변환기")
st.write("WAV 파일을 업로드하면 음성을 텍스트로 변환하고 번역해드립니다.")

# 언어 선택
language_option = st.selectbox("음성의 언어를 선택하세요:", ["한국어", "영어"])

# 언어 코드 설정
lang_code = {"한국어": "ko", "영어": "en"}[language_option]

# 파일 업로드
uploaded_file = st.file_uploader("WAV 파일 업로드", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_filename = tmp_file.name

    # 음성 인식
    recognizer = sr.Recognizer()
    with sr.AudioFile(tmp_filename) as source:
        audio = recognizer.record(source)

    try:
        # 텍스트 변환
        text = recognizer.recognize_google(audio, language=lang_code)
        st.subheader("📝 인식된 텍스트:")
        st.write(text)

        # 번역
        translator = Translator()
        translated = translator.translate(text, src=lang_code, dest="ko" if lang_code == "en" else "en")

        st.subheader("🌍 번역된 텍스트:")
        st.write(translated.text)

    except sr.UnknownValueError:
        st.error("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        st.error(f"Google 음성 인식 서비스에 접근할 수 없습니다: {e}")
    finally:
        os.remove(tmp_filename)
