import pyttsx3
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

byes()