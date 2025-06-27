#import
import streamlit as st
import speech_recognition as sr
import pyttsx3

#object creation
engine = pyttsx3.init()
recognizer = sr.Recognizer()

st.title("Say the wake word(Lucy)")

#function to print to terminal and speak to user
def speak_personalized(text):
    st.text(text)
    engine.say(text)
    engine.runAndWait()

# This function confirms with user its actions
def confirm_and_execute(intent):
    confirmation = f"Do you want me to switch {intent['action']} the {intent['device']} in the {intent['location']}?"
    speak_personalized(confirmation)   # Function call to speak and print confirmation message 

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5,phrase_time_limit=8)
            reply = recognizer.recognize_google(audio).lower()
            y = ["yes", "sure", "okay", "go ahead","do it","ok","please"]
            if any(w in reply for w in y):
                response = f"Okay, switching {intent['action']} the {intent['device']} in the {intent['location']}"
            else:
                response = "Command cancelled."
            st.text(f"User replied: {reply.strip().capitalize()}")

        #here user gets another chance to confirm the action 
        except:
            speak_personalized("I didn’t catch that. Would you like to try again?")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                retry_reply = recognizer.recognize_google(audio).lower()
                y = ["yes", "sure", "okay", "go ahead", "do it", "ok", "please"]

                if any(w in retry_reply for w in y):
                    response = f"Okay, switching {intent['action']} the {intent['device']} in the {intent['location']}"
                else:
                    response = "Command cancelled."
                st.text(f"User replied: {retry_reply.strip().capitalize()}")

            except:
                response = "Still couldn't get that. Skipping the action."

    speak_personalized(response)   #Function call to speak and print the result after conforming the message 

# this function says "Hi,what can i do for you"
def lucy_reacts():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    lucy_says = "Hi, how may I help you?"
    speak_personalized(lucy_says)   #Function call to speak and print "Hi, how may I help you?"
    ready_to_read_command()   # Function call to read  command from user

# This function reads user command
def ready_to_read_command():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("say somthing")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                txt = recognizer.recognize_google(audio)
                print("You said:", txt)
                st.text(f"You said: {txt}")
                if lucy_reply(txt):   # checks if the txt is bye if so then exits
                    break   # This break is for the loop that checks if txt is bye,if its bye then break else keeps hearing.
                intend = txt_to_intent(txt)   # function call to return intent to a variable

            except sr.WaitTimeoutError:
                speak_personalized("You were silent. Goodbye!")   # Function call to speak and print "You were silent. Goodbye!"
                break
            except sr.UnknownValueError:
                speak_personalized("Sorry, I couldn't get you. Come again.")   # Function call to speak and print " Sorry, I couldn't get you. Come again."
            except sr.RequestError:
                lucy_says_bye()   # Function call to lucy says bye
                break

#function for lucy saying bye
def lucy_says_bye():
    speak_personalized("Thank you, Good-Bye")   #Function call to speak and print bye

# this function is where lucy checks if users command is "bye"
def lucy_reply(user_words):
    a = ["tata", "bye", "bye-bye", "thank you for the service", "thank you", "see you later", "goodbye", "good night", "stop", "thank", "see you"]
    for w in a:
        if w in user_words.lower():
            lucy_says_bye()   #Function call to speak and print bye
            return True
    return False

# This function finds user command and forms intent out of it
def txt_to_intent(text):
    t = text.lower()
    intent = {"device": None, "action": None, "location": None}
    device_keyword = {
        "light": ["light", "bulb", "tubelight", "lamp"]
    }
    action_keyword = {
        "on": ["turn on", "switch on", "open", "play", "on", "run the", "start"],
        "off": ["turn off", "switch off", "close", "pause", "off", "don't run the", "terminate"]
    }
    location_keyword = {
        "hall": ["main room", "hall", "main"],
        "kitchen": ["kitchen"],
        "parent bedroom": ["main bedroom", "parent bedroom", "bedroom"],
        "bedroom": ["kids bedroom", "second bedroom"],
        "main bathroom": ["main bathroom", "bathroom", "washroom", "toilet"],
        "bathroom": ["kids bathroom", "second bathroom", "second washroom", "second toilet"]
    }

    for device, keywords in device_keyword.items():
        for keyword in keywords:
            if keyword in t:
                intent["device"] = device
                break
    for action, keywords in action_keyword.items():
        for keyword in keywords:
            if keyword in t:
                intent["action"] = action
                break
    for location, keywords in location_keyword.items():
        for keyword in keywords:
            if keyword in t:
                intent["location"] = location
                break

    if intent["device"] and intent["action"] and intent["location"]:
        confirm_and_execute(intent)   # Funtion call in which lucy asks user for confirmation
    else:
        missing_parts = []
        if not intent["device"]:
            missing_parts.append("device")
        if not intent["action"]:
            missing_parts.append("action")
        if not intent["location"]:
            missing_parts.append("location")

        if missing_parts:
            issue = " and ".join(missing_parts)
            speak_personalized(f"Please specify the {issue.capitalize()} in your command.")    #function call to speak and print which part of command is not specified.


# Main Loop heres where lucy is called upon as wake word
while True:
    with sr.Microphone() as source:
        print("Say the wake word 'Lucy'...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            txt = recognizer.recognize_google(audio)
            print("You said:", txt)
            st.text(f"You said: {txt}")
            b = ["lucy","Roxie","beauty","duty","chitti"]
            for w in b:
                if w in txt.lower():
                    lucy_reacts()   # Function call after it hears the word Beauty

                if lucy_reply(txt):     # Function call to check if its says bye 
                    break

        except sr.UnknownValueError:
            st.text("Didn't catch that. Please say the wake word again.")

        except sr.WaitTimeoutError:
            st.text("No input detected. Waiting again...")

        except sr.RequestError as e:
            st.text("Speech recognition service unavailable.")
            lucy_says_bye()   # Function call for lucy saying bye
            break

        except Exception as e:
            st.text("An unexpected error occurred.")
