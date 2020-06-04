import speech_recognition as sr


def speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    try:
        print("Audio text: " + text)
        f = open("speech.txt", "w")
        f.write(text)
        f.close
        return True
    except:
        return False
