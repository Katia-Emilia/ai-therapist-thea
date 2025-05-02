
import speech_recognition as sr
import pyttsx3

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from core import  handle_user_mood

# Initialize pyttsx3 for TTS
engine = pyttsx3.init()
# Set a female voice if available
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():  # "Zira" is the default female voice on Windows
        engine.setProperty('voice', voice.id)
        break
# Initialize SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Function for text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function for speech-to-text
def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            print("Listening for your voice...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=5)
            
        text = recognizer.recognize_google(audio)
        print("User: " + text)
        #speak("You said: " + text)
        return text
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand. Please repeat.")
        return ""
    except sr.RequestError:
        speak("Sorry, the service is down.")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""



# Voice Mode Interaction
def voice_mode(name, choice):
    print("Starting voice mode...")
    speak(f"Hi {name}, I am Thea, your therapist for today. Let's talk!")

    #user_emotion = "neutral"

    # Start emotion detection in a separate thread
    # threading.Thread(target=start_fake_video_call_and_listen).start()

    while True:
        user_input = listen()

        if user_input.lower() in ['exit', 'quit', 'bye', 'ok thank you for the session','ok bye','bye thank you']:
            speak("Goodbye! Take care!")
            break

        if user_input.strip() == "":
            continue  # if nothing heard, skip

        handle_user_mood(user_input, choice, detected_emotion=None)
        

        #speak(response)

    
