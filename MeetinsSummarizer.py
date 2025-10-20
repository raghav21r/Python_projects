from transformers import pipeline
import speech_recognition as s
import time
import pyttsx3
import datetime
intializer=pyttsx3.init('sapi5')
sound=intializer.getProperty('voices')
intializer.setProperty('voice',sound[0].id)
def talk(audio):#the role of this function is to accept the audio or text given or said by the user and generate the same by ai
    intializer.say(audio)
    intializer.runAndWait()
def greetings():#based on the current time it greets us
    clock=int(datetime.datetime.now().hour)

    if clock>=0 and clock<12:
        talk("good morning")
    elif clock>=12 and clock<18:
        talk("good afternoon")
    else:
        talk("good evening")
    talk('our project name is ')
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
greetings()
i=0
textt=''
if textt!='':
    summary=pipeline('summarization',model="sshleifer/distilbart-cnn-12-6")
    ss=summary(textt, max_length=200, do_sample=False)
    print(ss[0]['summary_text'])
else:
  while i<1:
    task=listen()
    textt+=task+''
    if "finish" in task.lower() or "stop" in task.lower():
        break
    i+=1
talk("Recording finished let's summerize")
summary=pipeline('summarization',model="sshleifer/distilbart-cnn-12-6")
ss=summary(textt, max_length=200, do_sample=False)
print(ss[0]['summary_text'])
voice=pipeline("automatic_speech_recognition")
Text=voice('enter an mp3 file')
print(Text)
