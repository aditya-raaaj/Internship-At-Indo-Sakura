import streamlit as st
import speech_recognition as sr
import pyttsx3

# this function works after lucy says "Hi,what can i do for you"
def lucy_reacts():
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    lucy_says = "Hi , How may I help you?"
    engine.say(lucy_says)
    st.text(lucy_says)
    engine.runAndWait()
    ready_to_read_command()


def ready_to_read_command():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("say somthing ")   # User commands is listened here
            recognizer.adjust_for_ambient_noise(source, duration=1)  

            try:
                audio = recognizer.listen(source, timeout = 5,phrase_time_limit=8)
                txt= recognizer.recognize_google(audio)
                print("You said ",txt)
                st.text(f"You said :{txt}")
                if lucy_reply(txt):   # This breaks the loop checks if txt is bye,if its bye then break else keeps hearing
                    break

                intend = txt_to_intent(txt)   # function called for turning off or on lights
                print(intend)

            except sr.WaitTimeoutError:
                print("Listening timed out, no speech detected.")
                engine.say("You were silent. Goodbye!")   # here lucy waits for a limited time and says "bye"
                st.text("You were silent. Goodbye!")
                engine.runAndWait()
                break

            except sr.UnknownValueError:
                print("Coudnt decode")   # here lucy says "Sorry,i didnt get you"
                engine.say("Sorry, I Couldn't get you. Come again.")
                st.text("Sorry, I Couldn't get you. Come again.")
                engine.runAndWait()
                
            except sr.RequestError:
                print("request timeout")
                lucy_says_bye()
                break
                   

#function for lucy saying bye
def lucy_says_bye():
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.say("Thank you , Good-Bye")
    st.text("Thank you , Good-Bye")
    engine.runAndWait()


# this function is where lucy checks if users command is "bye"
def lucy_reply(user_words):
    a = ["tata","bye","bye-bye","thank you for the service","thank you","see you later","goodbye","good night","stop"]
    for w in a:
        if w in user_words.lower():
            lucy_says_bye()
            return True
    return False  # here lucy replies for users "bye" and says "bye"


# function where lucy switches on or off the light
def txt_to_intent(text):
    t = text.lower()
    intent={"device":None,"action":None,"location":None}

    device_keyword={
        "light":["light","bulb","tubelight","lamp"]
    }
    action_keyword={
        "on":["turn on","switch on","open","play","on","run the","start"],
        "off":["turn off","switch off","close","pause","off","dont run the","terminate"]
    }
    location_keyword={
        "hall":["main room","hall","main"],
        "kitchen":["kitchen"],
        "parent bedroom":["main bedroom","parent bedroom","bedroom"],
        "bedroom":["kids bedroom","second bedroom"],
        "main bathroom":["main bathroom","bathroom","washroom","toilet"],
        "bathroom":["kids bathroom","second bathroom","second washroom","second toilet"]
    }

    for device,keywords in device_keyword.items():
        for keyword in keywords:
            if keyword in t:
                intent["device"]=device
                break
    
    for action,keywords in action_keyword.items():
        for keyword in keywords:
            if keyword in t:
                intent["action"]=action
                break

    for location,keywords in location_keyword.items():
        for keyword in keywords:
            if keyword in t:
                intent["location"]=location
                break
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    if intent["device"] and intent["action"] and intent["location"]:
        response = f"Okay, switching {intent['action']} the {intent['device']} in {intent['location']}"
    else:
        response = "Sorry, I didn't get the full command."
    st.text(f"Okay, switching {intent['action']} the {intent['device']} in {intent['location']}")
    engine.say(response)
    engine.runAndWait()
    # here lucy should reply with "okay switching on/off the lights in x(location)""
    return(intent)


#the code is always hearing once it hears "lucy" its triggered
engine=pyttsx3.init()
recognizer = sr.Recognizer()
st.title("Say the Wake word")
while True:
    with sr.Microphone() as source:
        print("say the wake word ")
        audio = recognizer.listen(source, timeout = 200,phrase_time_limit=200)
        try:
            txt= recognizer.recognize_google(audio)
            print("You said ",txt)
            st.text(txt)
            if "duty" in txt.lower():
                lucy_reacts() # lucy says "Hi,what can i do for you"
        except:
            if lucy_reply(txt):
                break
        