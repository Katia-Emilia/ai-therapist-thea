# import datetime
# import speech_recognition as sr
# import pyttsx3
# from mood import (happy_list, sad_list, angry_list, depressed_list, suicidal_list, happy_mood_responses, sad_mood_responses, angry_mood_responses, depressed_mood_responses, suicidal_mood_responses, general_responses)
# from functions import (wishme, takecommand, speak_and_print, speak)
# import cv2
# import threading
# from deepface import DeepFace
# import time

# choice = 2  #choice for voice chat
# listening = False  #to prevent multiple overlapping mic recordings


# def respond_to_emotion(dominant_emotion):
#     if dominant_emotion == "happy":
#         speak_and_print("It looks like you're feeling happy today. That's great to hear!",choice)
#     elif dominant_emotion == "sad":
#         speak_and_print("I can see you're feeling sad. Want to talk about what's going on?",choice)
#     elif dominant_emotion == "angry":
#         speak_and_print("You seem angry. It's okay to feel that way. Let's explore what might be causing that.",choice)
#     elif dominant_emotion == "surprise":
#         speak_and_print("You look surprised. What has caught your attention?",choice)
#     elif dominant_emotion == "fear":
#         speak_and_print("It seems you're feeling anxious. Would you like to share what's bothering you?",choice)
#     elif dominant_emotion == "disgust":
#         speak_and_print("It seems like something is upsetting you. Let's talk about it.",choice)
#     elif dominant_emotion == "neutral":
#         speak_and_print("I can see you're feeling calm. It's a good place to start a conversation.",choice)


# def handle_user_mood(user_statement, detected_emotion):
#     triggered = False

#     # First, try to detect from words
#     if any(word in user_statement for word in happy_list):
#         happy_mood_responses()
#         triggered = True

#     elif any(word in user_statement for word in sad_list):
#         sad_mood_responses()
#         triggered = True

#     elif any(word in user_statement for word in angry_list):
#         angry_mood_responses()
#         triggered = True

#     elif any(word in user_statement for word in depressed_list):
#         depressed_mood_responses()
#         triggered = True

#     elif any(word in user_statement for word in suicidal_list):
#         suicidal_mood_responses()
#         triggered = True

#     # If no word matches, use detected face emotion
#     if not triggered and detected_emotion:
#         respond_to_emotion(detected_emotion)

#     # If still nothing detected
#     if not triggered and not detected_emotion:
#         general_responses()

# def listen_in_thread(detected_emotion):
#     global listening
#     listening = True
#     user_statement = takecommand().lower()
#     try:
#         user_statement = takecommand().lower()
#         print(f"User said: {user_statement}")
#         handle_user_mood(user_statement, detected_emotion)
#     except Exception as e:
#         print(f"Error capturing speech: {e}")
#     listening = False
# def start_fake_video_call_and_listen():
#     global listening

#     cap = cv2.VideoCapture(0)
#     last_emotion = None
#     last_response_time = time.time()
#     frame_count = 0

#     def emotion_analysis(frame):
#         try:
#             temp_file = "temp_frame.jpg"
#             cv2.imwrite(temp_file, frame)
#             result = DeepFace.analyze(temp_file, actions=['emotion'], enforce_detection=False)
#             return result[0]['dominant_emotion']
#         except Exception as e:
#             print(f"Emotion analysis error: {e}")
#             return None

#     def listen_and_respond(emotion):
#         global listening
#         listening = True
#         try:
#             user_statement = takecommand().lower()
#             print(f"User said: {user_statement}")
#             handle_user_mood(user_statement, emotion)
#         except Exception as e:
#             print(f"Speech recognition error: {e}")
#         listening = False

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Only analyze every 10 frames for performance
#         if frame_count % 100 == 0:
#             dominant_emotion = emotion_analysis(frame)
#             if dominant_emotion and dominant_emotion != last_emotion:
#                 last_emotion = dominant_emotion

#         # Display emotion label
#         if last_emotion:
#             cv2.putText(frame, f'Emotion: {last_emotion}', (10, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         cv2.imshow("Thea - Video Therapy", frame)
#         frame_count += 1

#         # Every 6 seconds, listen (in a separate thread)
#         if time.time() - last_response_time > 30 and not listening:
#             print("Triggering speech recognition...")
#             threading.Thread(target=listen_and_respond, args=(last_emotion,)).start()
#             last_response_time = time.time()
        

#         # Exit condition
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # def start_fake_video_call_and_listen():
# #     cap = cv2.VideoCapture(0)
# #     last_emotion = None
# #     last_response_time = time.time()
# #     frame_count = 0

# #     while cap.isOpened():
# #         ret, frame = cap.read()
# #         if not ret:
# #             break

# #         # temp_file = "temp_frame.jpg"
# #         # cv2.imwrite(temp_file, frame)

# #         # Analyze the emotion from video
# #         frame_count += 1
# #         dominant_emotion = None

# #         if frame_count % 10 == 0:  # Analyze every 10 frames
# #             temp_file = "temp_frame.jpg"
# #             cv2.imwrite(temp_file, frame)
# #             try:
# #                 result = DeepFace.analyze(temp_file, actions=['emotion'], enforce_detection=False)
# #                 dominant_emotion = result[0]['dominant_emotion']
# #                 if dominant_emotion != last_emotion:
# #                     last_emotion = dominant_emotion
# #                     # cv2.putText(frame, f'Emotion: {dominant_emotion}', (10, 50),
# #                     #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
# #             except Exception as e:
# #                 print(f"Error analyzing emotion: {e}")
# #         if last_emotion:
# #             cv2.putText(frame, f'Emotion: {dominant_emotion}', (10, 50),
# #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

# #         # Show the frame
# #         cv2.imshow("Fake Video Call with Thea", frame)

# #         # Every few seconds, listen to user speech + analyze
# #         if time.time() - last_response_time > 5 and not listening:  # Every 5 seconds
# #             print("Listening for user input...")
# #             threading.Thread(target=listen_in_thread, args=(last_emotion,)).start()
            
# #             # user_statement = takecommand().lower()
# #             # print(f"User said: {user_statement}")

# #             # handle_user_mood(user_statement, dominant_emotion)

# #             last_response_time = time.time()

# #         if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break

# #     cap.release()
# #     cv2.destroyAllWindows()


# # Initialize the text-to-speech engine
# engine = pyttsx3.init()
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[1].id)

# # Call the wishme function to greet the user
# wishme()

# # Ask for the user's name and start the therapy session and desclaimer that say this is Not a real therapist just a script 
# # while True:
# #     speak_and_print("Before we proceed, please note that Thea is an AI therapist designed to provide support and companionship. It is not a substitute for professional mental health care. If you are experiencing severe distress or have suicidal thoughts, please seek immediate help from a mental health professional or contact a helpline in your region.",choice)

# #     speak_and_print("The Thea development team emphasizes that while Thea aims to be supportive, it is not a licensed therapist. The AI is continually learning and evolving, and your feedback is valuable for its improvement. The Thea team does not take responsibility for any harm caused by the program; use it at your own risk.",choice)

# #     disclaimer = "If you understand that Thea is not a real therapist and you have read and understood the disclaimer, please type 'y' to confirm: "

    
# #     speak_and_print(disclaimer,choice)
# #     user_agree = input("type hear: ").lower()
    
# #     if user_agree == "y":
# #         break  # Break out of the loop if the user agrees to the terms of service
# #     elif user_agree == "admin code 110308":
# #         break

# # Proceed with the therapy session
# speak_and_print("Now, please state your name for easy communication",choice)
# name = input("Your Name: ")

# while True:
#     print("1. Text Chat")
#     print("2. Voice Call")
#     print("3. Video Call") 
#     choice = int(input("Choose an option (1/2/3): "))

#     if choice == 1 or choice == 2 or choice == 3:
#         break
#     else:
#         speak_and_print("Please choose a valid option.",choice)  
# #the session has started after the introduction
# speak_and_print(f"I am Thea, your therapist for today, {name} remember that you can end the session whenever you what by saying `ok thank you for the session` to . Let's start. How are you feeling today?",choice)

# # Main program execution
# if __name__ == "__main__":
#     while True:
#         if choice==1 or choice== 2:
#             if choice==1:
#                 user_statement = input("User: ").lower()
#             elif choice==2:
#                 user_statement = takecommand().lower()

#             # Check user's statement against mood lists and provide responses
#             if any(word in user_statement for word in happy_list):
#                 happy_mood_responses()

#             elif any(word in user_statement for word in sad_list):
#                 sad_mood_responses()

#             elif any(word in user_statement for word in angry_list):
#                 angry_mood_responses()

#             elif any(word in user_statement for word in depressed_list):
#                 depressed_mood_responses()

#             elif any(word in user_statement for word in suicidal_list):
#                 suicidal_mood_responses()
                
#             elif user_statement == "ok thanks for the session":
#                 speak_and_print("Ok then see you next time",choice)
#                 break
                
#             if all(word not in user_statement for word in happy_list + sad_list + angry_list + depressed_list + suicidal_list):
#                 general_responses()
#         if choice==3:
#             start_fake_video_call_and_listen()


import datetime
import speech_recognition as sr
import pyttsx3
from mood import (happy_list, sad_list, angry_list, depressed_list, suicidal_list,
                  happy_mood_responses, sad_mood_responses, angry_mood_responses,
                  depressed_mood_responses, suicidal_mood_responses, general_responses)
from functions import (wishme, takecommand, speak_and_print, speak)
import cv2
import threading
from deepface import DeepFace
import time

# Initial Setup
choice = 2  # 1 = text, 2 = voice, 3 = video
listening = False


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
        speak_and_print(responses[dominant_emotion], choice)


def handle_user_mood(user_statement, detected_emotion):
    triggered = False

    if any(word in user_statement for word in happy_list):
        happy_mood_responses()
        triggered = True
    elif any(word in user_statement for word in sad_list):
        sad_mood_responses()
        triggered = True
    elif any(word in user_statement for word in angry_list):
        angry_mood_responses()
        triggered = True
    elif any(word in user_statement for word in depressed_list):
        depressed_mood_responses()
        triggered = True
    elif any(word in user_statement for word in suicidal_list):
        suicidal_mood_responses()
        triggered = True

    if not triggered and detected_emotion:
        respond_to_emotion(detected_emotion)
    elif not triggered:
        general_responses()


def listen_and_respond(emotion):
    global listening
    listening = True
    try:
        user_statement = takecommand().lower()
        print(f"User said: {user_statement}")
        if "ok thank you for the session" in user_statement:
            speak_and_print("Ok then see you next time", choice)
            exit()
        handle_user_mood(user_statement, emotion)
    except Exception as e:
        print(f"Speech recognition error: {e}")
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

        if frame_count % 100 == 0:
            dominant_emotion = emotion_analysis(frame)
            if dominant_emotion and dominant_emotion != last_emotion:
                last_emotion = dominant_emotion

        if last_emotion:
            cv2.putText(frame, f'Emotion: {last_emotion}', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Thea - Video Therapy", frame)
        frame_count += 1

        if time.time() - last_response_time > 30 and not listening:
            print("Triggering speech recognition...")
            threading.Thread(target=listen_and_respond, args=(last_emotion,)).start()
            last_response_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ========== SESSION START ==========
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

wishme()

# Disclaimer
speak_and_print("Before we proceed, please note that Thea is an AI therapist designed to provide support and companionship. It is not a substitute for professional mental health care. If you are experiencing severe distress or have suicidal thoughts, please seek immediate help from a mental health professional or contact a helpline in your region.", choice)
speak_and_print("Thea is not a licensed therapist. Please use this tool with discretion. Type 'y' to continue.", choice)

user_agree = input("Type here to agree: ").lower()
if user_agree not in ["y", "admin code 110308"]:
    speak_and_print("Thank you. Exiting session.", choice)
    exit()

# Get user name
speak_and_print("Now, please state your name for easy communication", choice)
name = input("Your Name: ")

# Session type
while True:
    print("1. Text Chat")
    print("2. Voice Call")
    print("3. Video Call")
    choice = int(input("Choose an option (1/2/3): "))
    if choice in [1, 2, 3]:
        break
    else:
        speak_and_print("Please choose a valid option.", choice)

speak_and_print(f"I am Thea, your therapist for today, {name}. Remember, you can end the session anytime by saying or typing `ok thank you for the session`. Let's start. How are you feeling today?", choice)

# Main Execution
if __name__ == "__main__":
    while True:
        if choice == 1:
            user_statement = input("User: ").lower()
        elif choice == 2:
            user_statement = takecommand().lower()
        elif choice == 3:
            start_fake_video_call_and_listen()
            break  # Exit after video session ends

        if "ok thank you for the session" in user_statement:
            speak_and_print("Ok then see you next time", choice)
            break

        handle_user_mood(user_statement, detected_emotion=None)
