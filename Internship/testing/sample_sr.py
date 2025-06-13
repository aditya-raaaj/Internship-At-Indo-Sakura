#working speech to text and showing the intent
import speech_recognition as sr
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("say somthing ")
    audio = recognizer.listen(source)
    try:
        txt= recognizer.recognize_google(audio)
        print("u said ",txt)
    except sr.UnknownValueError:
        print("Coudnt decode")
    except sr.RequestError:
        print("request timeout")
    

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
        "parent_bedroom":["main bedroom","parent_bedroom","bedroom"],
        "bedroom":["kids bedroom","second bedroom"],
        "main_bathroom":["main bathroom","bathroom","washroom","toilet"],
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
    return(intent)

intend = txt_to_intent(txt)
print(intend)
