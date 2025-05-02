
from core import handle_user_mood, start_fake_video_call_and_listen

from functions import (wishme)


# Initial Setup
listening = False


def run_voice_mode(name,choice):
    from voice_mode import voice_mode
    voice_mode(name,choice)




# ========== SESSION START ==========
choice=1
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

while True:
    print("1. Text Chat")
    print("2. Text Chat with Emotion Detection")
    print("3. Voice Chat ")
    choice = int(input("Choose an option (1/2/3): "))
    if choice in [1, 2, 3, ]:
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
        elif choice==3:
            run_voice_mode(name,choice)
            break

        handle_user_mood(user_statement, choice,detected_emotion=None)
        if "ok thank you for the session" in user_statement:
            print("Ok then see you next time")
            break

        

        
