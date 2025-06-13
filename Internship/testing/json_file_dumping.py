import json
ldata=[]
txt = input("enter the command: ")
device = input("enter the device: ")
action = input("enter the action: ")
data={
    "command" : txt,
    "device" :device,
    "action" : action
}
ldata.append(data)
with open("labeled_intents.json","w") as f:
    json.dump(ldata,f,indent=4)
with open("labeled_intents.json","r") as r:
    d=r.read()
    print(d)