
import datetime

# Function to greet the user based on the time of day
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print("Good morning!")
        
    elif 12 <= hour < 18:
        print("Good afternoon")
        
    elif 18 <= hour < 21:
        print("Good evening!")
        
    else:
        print("Good night")