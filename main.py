
import eel
import speech_recognition as sr
import pyttsx3
import openai
from datetime import datetime

# === SET YOUR OPENAI API KEY ===
openai.api_key = "your-openai-api-key"

# Initialize Eel
eel.init('web')
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    eel.show_response(text)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def start_voice():
    with sr.Microphone() as source:
        eel.set_status("Listening...")
        audio = recognizer.listen(source, timeout=5)
    try:
        text = recognizer.recognize_google(audio)
        eel.display_user(text)
        process(text)
    except Exception as e:
        speak("Sorry, I couldn't understand that.")

@eel.expose
def process(text):
    try:
        eel.set_status("Thinking...")
        # GPT response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named BOTIQ."},
                {"role": "user", "content": text}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        reply = "I'm sorry, I couldn't connect to GPT right now."
    
    speak(reply)
    eel.set_status("Idle")

# Voice + text intro when app starts
def welcome():
    eel.show_response("Hello, I am BOTIQ")
    speak("Hello, I am BOTIQ")

eel.start('index.html', size=(900, 600), block=False)
welcome()
while True:
    eel.sleep(1)
