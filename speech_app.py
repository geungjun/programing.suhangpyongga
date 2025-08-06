programing.suhangpyongga/
speech_app.py
requirements.txt      
README.md



import speech_recognition as sr

def get_language():
    print("\n🌐 사용할 언어를 선택하세요.")
    print("1. 한국어 (ko-KR)")
    print("2. 영어 (en-US)")
    lang_choice = input("선택 (1 또는 2): ")
    if lang_choice == "1":
        return "ko-KR"
    elif lang_choice == "2":
        return "en-US"
    else:
        print("❌ 잘못된 선택입니다. 기본값 'ko-KR'로 설정합니다.")
        return "ko-KR"

def recognize_from_mic(language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ 마이크가 켜졌습니다. 말을 해주세요.")
        print("※ 조용한 환경에서 또박또박 말하면 더 정확합니다.")
        audio = r.listen(source)
        print("🔍 인식 중입니다. 잠시만 기다려주세요...")

    try:
        text = r.recognize_google(audio, language=language)
        print("\n📝 인식된 문장:")
        print(text)
    except sr.UnknownValueError:
        print("❌ 음성을 인식할 수 없습니다. 다시 시도해주세요.")
    except sr.RequestError:
        print("⚠️ 인식 서버에 접근할 수 없습니다. 인터넷 연결을 확인하세요.")

def recognize_from_file(language):
    r = sr.Recognizer()
    print("\n📁 파일을 통해 음성을 입력합니다.")
    print("※ WAV 형식의 파일을 사용하는 것을 권장합니다.")
    filename = input("파일 경로를 입력하세요 (예: sample.wav): ")

    try:
        with sr.AudioFile(filename) as source:
            print("🔍 인식 중입니다. 잠시만 기다려주세요...")
            audio = r.record(source)
        text = r.recognize_google(audio, language=language)
        print("\n📝 인식된 문장:")
        print(text)
    except FileNotFoundError:
        print("❌ 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    except sr.UnknownValueError:
        print("❌ 음성을 인식할 수 없습니다.")
    except sr.RequestError:
        print("⚠️ 인식 서버에 접근할 수 없습니다.")

def main():
    print("🎧 음성 인식 프로그램")
    print("1. 마이크로 직접 입력")
    print("2. 음성 파일로 입력")
    choice = input("선택하세요 (1 또는 2): ")

    language = get_language()

    if choice == "1":
        recognize_from_mic(language)
    elif choice == "2":
        recognize_from_file(language)
    else:
        print("❌ 잘못된 선택입니다. 프로그램을 종료합니다.")

if __name__ == "__main__":
    main()
