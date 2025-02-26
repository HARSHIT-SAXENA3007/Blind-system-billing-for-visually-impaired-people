import speech_recognition as sr
import pyttsx3
def listen():
    with sr.Microphone() as source:
        status_label.configure(text="Listening...")
        speak("speak now")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            status_label.configure(text=f"User said: {command}")
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            status_label.configure(text="Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return None
