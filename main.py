import eel
import pyttsx3
import speech_recognition as sr
import openai

# === SET YOUR OPENAI API KEY BELOW ===
# Replace the text inside the quotes with your actual OpenAI key
openai.api_key = "your-api-key-here"

# Initialize Eel
eel.init("web")

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    """Speak text and display in frontend"""
    try:
        eel.show_response(text)()
    except Exception:
        pass
    engine.say(text)
    engine.runAndWait()

@eel.expose
def process(text):
    """Send user text to GPT and return reply using OpenAI >=1.0.0 API"""
    try:
        eel.set_status("🤔 Thinking...")()
        chat = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named BOTIQ."},
                {"role": "user", "content": text},
            ],
        )
        reply = chat.choices[0].message.content
    except Exception as e:
        reply = f"🚨 GPT Error: {e}"
    speak(reply)
    eel.set_status("✅ Idle")()

@eel.expose
def start_voice():
    """Listen from microphone and process speech"""
    with sr.Microphone() as source:
        try:
            eel.set_status("🎤 Listening...")()
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            eel.display_user(text)()
            process(text)
        except Exception as e:
            speak(f"Sorry, I couldn't understand that. Error: {e}")
        finally:
            eel.set_status("Idle")()

@eel.expose
def start_welcome():
    speak("Hello, I am BOTIQ. How can I help you today?")

if __name__ == "__main__":
    eel.start("index.html", size=(900, 600), port=8080)
