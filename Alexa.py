import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import pyaudio
import time
import pytz
import mysql.connector
import functools
import operator

from datetime import datetime, timedelta

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

now = datetime.now()
now2 = now + timedelta(seconds=80)
current_time1 = now2.strftime("%H")
current_time2 = now2.strftime("%M")


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening.....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    global c
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song + 'on youtube')
        pywhatkit.playonyt(song)
    elif 'time' in command:
        curr_time = time.localtime()
        curr_clock = time.strftime("%I:%M %p", curr_time)
        print("The current time is " + curr_clock)
        talk("Current time is " + curr_clock)
    elif 'search' in command:
        person = command.replace('search', '')
        info = wikipedia.summary(person, 3)
        print(info)
        talk(info)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 3)
        print(info)
        talk(info)
    elif 'find' and 'wikipedia' in command:
        person = command.replace('find', '')
        person = command.replace('wikipedia', '')
        info = wikipedia.summary(person, 3)
        print(info)
        talk(info)
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)
    elif 'stop' in command:
        exit()
    elif 'send whatsapp message to' in command:
        print(command)
        person1 = command.replace('send whatsapp message to', '')
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="445712", database="shivam")
        mycursor = mydb.cursor()

        def convertTuple(tup):
            str1 = functools.reduce(operator.add, tup)
            return str1

        person1 = person1.strip()
        mycursor.execute("select phone from phonebook where name = '%s'" % person1)
        for i in mycursor:
            str2 = convertTuple(i)
            print(str2)
        talk("What do you want to send?")
        print("What do you want to send?")
        print("Listening.....")
        try:
            with sr.Microphone() as source:
                voice = listener.listen(source)
                command2 = listener.recognize_google(voice)
                command2 = command2.lower()
                print(command2)
                talk('sending' + person1 + 'whatsapp message')
                pywhatkit.sendwhatmsg(str2, command2, int(current_time1), int(current_time2))
        except:
            pass

    else:
        talk("Sorry. I don't know that one")


run_alexa()
