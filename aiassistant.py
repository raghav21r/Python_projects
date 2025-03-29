#jai shree ram
import pyttsx3
import os
import datetime
import time
import speech_recognition as s
import wikipedia as wp
import webbrowser as wb
import smtplib
intializer=pyttsx3.init('sapi5')
sound=intializer.getProperty('voices')
intializer.setProperty('voice',sound[0].id)
def talk(audio):#the role of this function is to accept the audio or text given or said by the user and generate the same by ai
    intializer.say(audio)
    intializer.runAndWait()
def greetings():#based on the current time it greets us 
    clock=int(datetime.datetime.now().hour)
    talk("jai shree ram")
    if clock>=0 and clock<12:
        talk("good morning")
    elif clock>=12 and clock<18:
        talk("good afternoon")
    else:
        talk("good evening")
    talk("how may i assist you")
def listen():#this fuction is responsible for analyzing the voice that we said
    r=s.Recognizer()
    with s.Microphone() as source:
        print("speak...")
        r.pause_threshold=1
        sound=r.listen(source)
    try:
        task=r.recognize_google(sound,language='en-in')
        time.sleep(1)
    except Exception as e:
        talk("sorry i didn't get you")
        return "None"
    return task
if __name__=="__main__":
    greetings()
    i=0
    while i<1:
        task=listen().lower()
        if "youtube" in task:
            wb.open("https://youtube.com")
            i+=1
        elif "edge" in task:
            wb.open("micrsoftedge.com")
            i+=1
        elif "google" in task:
            wb.open("http://google.com")
            i+1
        elif "whats" in task:
            wb.open("https://web.whatsapp.com/")
            i+=1
        elif "time" in task:
            t=datetime.datetime.now().strftime("%H:%M")
            talk(f"the time is {t}")
            i+=1
        elif "zoom" in task:
            address="Users\\nitish\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
            os.startfile(address)
            i+=1
        elif "ide" in task:
            path="C:\\Users\\nitish\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(path)
            i+=1
        else:
            rs=wp.summary(task,sentences=2)
            talk(rs)
            print(rs)
            i+=1