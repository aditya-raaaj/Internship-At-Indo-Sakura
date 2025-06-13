'''import pyttsx3
engine = pyttsx3.init()
rate = engine.getProperty('rate')
print(rate)
engine.setProperty('rate',135)
voices= engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.say("Hi,what can i help you with?")
engine.runAndWait() # here its case sensitive A andW are caps



def byes():
    engine.say("Hi , How are you")
    engine.runAndWait()

byes()'''

import speech_recognition as sr
import pyttsx3

# Initialize the speech engine once
engine = pyttsx3.init()

# Say goodbye
def lucy_says_bye():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say("Thank you, Bye")
    engine.runAndWait()

# Check if the user says "bye"
def lucy_reply(user_words):
    if "bye" in user_words.lower():
        lucy_says_bye()
        return True  # Signal to stop
    return False  # Keep going

# Parse the user's intent
def txt_to_intent(text):
    t = text.lower()
    intent = {"device": None, "action": None, "location": None}

    device_keyword = {
        "light": ["light", "bulb", "tubelight", "lamp"]
    }
    action_keyword = {
        "on": ["turn on", "switch on", "open", "play", "on", "run the", "start"],
        "off": ["turn off", "switch off", "close", "pause", "off", "don't run", "terminate"]
    }
    location_keyword = {
        "hall": ["main room", "hall", "main"],
        "kitchen": ["kitchen"],
        "parent_bedroom": ["main bedroom", "parent bedroom", "bedroom"],
        "bedroom": ["kids bedroom", "second bedroom"],
        "main_bathroom": ["main bathroom", "bathroom", "washroom", "toilet"],
        "bathroom": ["kids bathroom", "second bathroom", "second washroom", "second toilet"]
    }

    # Match keywords
    for device, keywords in device_keyword.items():
        if any(keyword in t for keyword in keywords):
            intent["device"] = device
            break

    for action, keywords in action_keyword.items():
        if any(keyword in t for keyword in keywords):
            intent["action"] = action
            break

    for location, keywords in location_keyword.items():
        if any(keyword in t for keyword in keywords):
            intent["location"] = location
            break

    # Voice reply
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    if intent["device"] and intent["action"] and intent["location"]:
        response = f"Okay, switching {intent['action']} the {intent['device']} in {intent['location']}"
    else:
        response = "Sorry, I didn't get the full command."
    engine.say(response)
    engine.runAndWait()
    return intent

# Read user's command and act
def ready_to_read_command():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Say something...")
            audio = recognizer.listen(source)
            try:
                txt = recognizer.recognize_google(audio)
                print("You said:", txt)

                if lucy_reply(txt):  # If user says "bye", stop
                    break

                intent = txt_to_intent(txt)
                print(intent)

            except sr.UnknownValueError:
                print("Couldn't understand")
                engine.say("Sorry, I couldn't get you. Come again.")
                engine.runAndWait()
            except sr.RequestError:
                print("Request timeout")
                lucy_says_bye()
                break

# Lucy greets and starts listening
def lucy_reacts():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say("Hi, what can I do for you?")
    engine.runAndWait()
    ready_to_read_command()

# Lucy waits for wake word
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Say the wake word (like 'duty')...")
    audio = recognizer.listen(source)
    try:
        txt = recognizer.recognize_google(audio)
        print("You said:", txt)
        if "duty" in txt.lower():
            lucy_reacts()
    except:
        lucy_says_bye()
