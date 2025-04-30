import datetime
from mood import (happy_list, sad_list, angry_list, depressed_list, suicidal_list,
                  happy_mood_responses, sad_mood_responses, angry_mood_responses,
                  depressed_mood_responses, suicidal_mood_responses, general_responses)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from functions import (wishme)
import cv2
import threading
from deepface import DeepFace
import time

# Initial Setup
listening = False

# Function to print sentiments of the sentence.
def sentiment_scores(sentence):

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.

    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict['compound']

def respond_to_emotion(dominant_emotion):
    responses = {
        "happy": "It looks like you're feeling happy today. That's great to hear!",
        "sad": "I can see you're feeling sad. Want to talk about what's going on?",
        "angry": "You seem angry. It's okay to feel that way. Let's explore what might be causing that.",
        "surprise": "You look surprised. What has caught your attention?",
        "fear": "It seems you're feeling anxious. Would you like to share what's bothering you?",
        "disgust": "It seems like something is upsetting you. Let's talk about it.",
        "neutral": "I can see you're feeling calm. It's a good place to start a conversation.",
    }
    if dominant_emotion in responses:
        print(responses[dominant_emotion])


def handle_user_mood(user_statement, detected_emotion):
    triggered = False

    if any(word in user_statement for word in happy_list):
        if detected_emotion == "happy":
            respond_to_emotion(detected_emotion)
        happy_mood_responses()
        triggered = True

    elif any(word in user_statement for word in sad_list):
        if detected_emotion == "sad" or detected_emotion=="fear":
            respond_to_emotion(detected_emotion)
        sad_mood_responses()
        triggered = True

    elif any(word in user_statement for word in angry_list):
        if detected_emotion == "angry":
            respond_to_emotion(detected_emotion)
        angry_mood_responses()
        triggered = True

    elif any(word in user_statement for word in depressed_list):
        if detected_emotion == "sad" or detected_emotion == "disgust":
            respond_to_emotion(detected_emotion)
        depressed_mood_responses()
        triggered = True

    elif any(word in user_statement for word in suicidal_list):
        if detected_emotion == "sad" or detected_emotion == "disgust":
            respond_to_emotion(detected_emotion)

        print("It seems you're in a very low state. Please remember that it's okay to seek help. I recommend talking to a professional therapist or counselor.")
        suicidal_mood_responses()
        triggered = True
    
    else:        
        sentiment_compound=sentiment_scores(user_statement)
        if sentiment_compound >= 0.05:
            print("It seems you're in a good mood. That's wonderful!")
            respond_to_emotion(detected_emotion)
        elif sentiment_compound <= -0.05:  
            print("It seems you're in a low mood. It's okay to feel that way. Let's talk about it.")
            respond_to_emotion(detected_emotion) 
        else:
            general_responses()
        triggered = True

    if not triggered and detected_emotion:
        respond_to_emotion(detected_emotion)
    

def respond(emotion):
    global listening
    listening = True
    try:
        user_statement = input("User: ").lower() 
        
        if "ok thank you for the session" in user_statement:
            print("Ok then see you next time")
            exit()
        handle_user_mood(user_statement, emotion)
    except Exception as e:
        print(f"Text recognition error: {e}")
    listening = False


def emotion_analysis(frame):
    try:
        temp_file = "temp_frame.jpg"
        cv2.imwrite(temp_file, frame)
        result = DeepFace.analyze(temp_file, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except Exception as e:
        print(f"Emotion analysis error: {e}")
        return None


def start_fake_video_call_and_listen():
    global listening
    cap = cv2.VideoCapture(0)
    last_emotion = None
    last_response_time = time.time()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 5 == 0:
            dominant_emotion = emotion_analysis(frame)
            if dominant_emotion and dominant_emotion != last_emotion:
                last_emotion = dominant_emotion
                

        if last_emotion:
            cv2.putText(frame, f'Emotion: {last_emotion}', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Thea - Video Therapy", frame)
        frame_count += 1

        if time.time() - last_response_time > 3 and not listening:
            print("Triggering speech recognition...")
            threading.Thread(target=respond, args=(last_emotion,)).start()
            last_response_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ========== SESSION START ==========
wishme()

# Disclaimer
print("Before we proceed, please note that Thea is an AI therapist designed to provide support and companionship. It is not a substitute for professional mental health care. If you are experiencing severe distress or have suicidal thoughts, please seek immediate help from a mental health professional or contact a helpline in your region.")
print("Thea is not a licensed therapist. Please use this tool with discretion. Type 'y' to continue.")

user_agree = input("Type here to agree: ").lower()
if user_agree not in ["y", "admin code 110308"]:
    print("Thank you. Exiting session.")
    exit()

# Get user name
print("Now, please state your name for easy communication")
name = input("Your Name: ")

# Session type
choice=2
while True:
    print("1. Text Chat")
    print("2. Text Chat with Emotion Detection")
    choice = int(input("Choose an option (1/2): "))
    if choice in [1, 2, ]:
        break
    else:
        print("Please choose a valid option.")

print(f"I am Thea, your therapist for today, {name}. Remember, you can end the session anytime by saying or typing `ok thank you for the session`. Let's start. How are you feeling today?")

# Main Execution
if __name__ == "__main__":
    while True:
        if choice == 1:
            user_statement = input("User: ").lower()
        elif choice == 2:
            start_fake_video_call_and_listen()
            break  # Exit after video session ends

        if "ok thank you for the session" in user_statement:
            print("Ok then see you next time")
            break

        handle_user_mood(user_statement, detected_emotion=None)
