import speech_recognition as sr


def speech_to_text(audio_file):
    r = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print("Audio text: " + text)
            f = open("speech.txt", "w")
            f.write(text)
            f.close
            return "Success"

    except ValueError as e:
        return e
    except Exception as e:
        return e
