import streamlit as st              # 스트림릿 앱 만들기 위한 라이브러리
import speech_recognition as sr    # 음성 인식 라이브러리
import tempfile                    # 업로드된 파일을 임시로 저장하기 위한 모듈

# ------------------------------
st.title("🎤 음성 파일 텍스트 변환기")   # 앱 제목 출력
st.write("WAV 음성 파일을 업로드하면 텍스트로 변환해드려요.")  # 설명글 출력

# ------------------------------
# ✅ 언어 선택 드롭다운
language_option = st.selectbox("음성의 언어를 선택하세요", ["한국어", "영어"])  
# 사용자에게 언어 선택하도록 하고 결과를 language_option에 저장

language_code = "ko-KR" if language_option == "한국어" else "en-US"  
# 선택된 언어에 따라 실제 인식에 사용할 언어코드 설정

# ------------------------------
# ✅ 파일 업로드 박스
uploaded_file = st.file_uploader("🎧 음성 파일을 업로드하세요 (WAV만 지원)", type=["wav"])  
# 사용자가 .wav 파일을 업로드할 수 있도록 업로더 제공

# ------------------------------
# 파일이 업로드되었을 때만 아래 코드 실행
if uploaded_file is not None:
    recognizer = sr.Recognizer()  
    # 음성 인식기 객체 생성

    # --------------------------
    # 업로드된 파일을 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())  
        # 업로드된 내용을 임시 파일로 저장
        temp_audio_path = temp_audio.name  
        # 저장된 임시 파일 경로 저장

    # --------------------------
    # 임시 파일을 열어서 음성 데이터를 읽음
    with sr.AudioFile(temp_audio_path) as source:
        st.info("음성을 분석 중입니다...")  # 진행 상황 메시지
        audio = recognizer.record(source)   # 전체 음성을 오디오 객체로 읽음

        try:
            # Google API를 사용해 선택한 언어로 텍스트 인식
            text = recognizer.recognize_google(audio, language=language_code)
            st.success("📝 인식된 텍스트:")  # 성공 메시지 출력
            st.write(text)  # 변환된 텍스트 보여줌

        except sr.UnknownValueError:
            # 인식 실패 (음성을 이해할 수 없는 경우)
            st.error("❌ 음성을 이해하지 못했어요.")

        except sr.RequestError as e:
            # Google API 요청 실패
            st.error(f"❌ Google API 요청 오류: {e}")
