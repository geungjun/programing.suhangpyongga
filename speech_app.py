import streamlit as st
import speech_recognition as sr
import tempfile

from googletrans import Translator

# ------------------------------
st.title("🎤 음성 텍스트 변환 + 번역기")
st.write("WAV 음성 파일을 업로드하면 텍스트로 변환하고 번역까지 해드려요.")

# ------------------------------
language_option = st.selectbox("음성의 언어를 선택하세요", ["한국어", "영어"])
language_code = "ko-KR" if language_option == "한국어" else "en-US"
target_lang = "ko" if language_option == "영어" else "en"

# ------------------------------
uploaded_file = st.file_uploader("🎧 음성 파일을 업로드하세요 (WAV만 지원)", type=["wav"])

if uploaded_file is not None:
    recognizer = sr.Recognizer()
    translator = Translator()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    with sr.AudioFile(temp_audio_path) as source:
        st.info("음성을 분석 중입니다...")
        audio = recognizer.record(source)

        try:
            # 음성 인식
            text = recognizer.recognize_google(audio, language=language_code)
            st.success("📝 인식된 텍스트:")
            st.write(f"{language_option}: {text}")

            # 번역
            translated = translator.translate(text, dest=target_lang)
            st.success("🌍 번역 결과:")
            st.write(f"{'한국어' if target_lang == 'ko' else '영어'}: {translated.text}")

        except sr.UnknownValueError:
            st.error("❌ 음성을 이해하지 못했어요.")
        except sr.RequestError as e:
            st.error(f"❌ Google API 요청 오류: {e}")
