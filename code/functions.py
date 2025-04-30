import pyttsx3
import speech_recognition as sr
import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Function to speak the given audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to print a message and speak it
def speak_and_print(message,choice):
    
        
    print(message)
    if choice==2 or choice==3:
        speak(message)

# Function to take microphone input and return string output
def takecommand():    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source)  # Adjusts to ambient noise levels
        
        print("Listening...")
        try:
            audio = r.listen(source,timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            speak_and_print("I didn’t hear anything. Please try again.", choice=2)
            return "None"
        except Exception as e:
            speak_and_print(f"Error while listening: {str(e)}", choice=2)
            return "None"


    try:
        print("Recognizing...")
        user_statement = r.recognize_google(audio, language="en-us")
        print(f"User side: {user_statement}\n")
        return user_statement.lower()  # Return as lowercase for consistency
    except sr.UnknownValueError:
        speak_and_print("Sorry, I couldn't understand that. Could you say it again?", choice=2)
        return "None"
    except sr.RequestError as e:
        speak_and_print(f"Service error: {str(e)}. Please try again later.", choice=2)
        return "None"
    except Exception as e:
        speak_and_print(f"Error during recognition: {str(e)}", choice=2)
        return "None"

# Function to greet the user based on the time of day
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak_and_print("Good morning!",choice=2)
        
    elif 12 <= hour < 18:
        speak_and_print("Good afternoon",choice=2)
        
    elif 18 <= hour < 21:
        speak_and_print("Good evening!",choice=2)
        
    else:
        speak_and_print("Good night",choice=2)