# OCEAN AI real

import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import threading
import time
from datetime import datetime
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

def speak(text):
    print("OCEAN:", text)
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""

def set_reminder(message, delay_seconds):
    def remind():
        time.sleep(delay_seconds)
        speak(f"Reminder: {message}")
    threading.Thread(target=remind).start()

def set_alarm(alarm_time):
    def alarm_check():
        while True:
            now = datetime.now().strftime("%H:%M")
            if now == alarm_time:
                speak("Wake up! It's time!")
                break
            time.sleep(30)
    threading.Thread(target=alarm_check).start()

def system_control(command):
    if "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif "lock" in command:
        speak("Locking the system.")
        os.system("rundll32.exe user32.dll,LockWorkStation")

def handle_command(command):
    if "time" in command:
        speak(f"The time is {datetime.now().strftime('%I:%M %p')}")
    elif "date" in command:
        speak(f"Today's date is {datetime.now().strftime('%B %d, %Y')}")
    elif "open notepad" in command:
        os.system("notepad.exe")
    elif "open calculator" in command:
        os.system("calc.exe")
    elif "search" in command:
        query = command.replace("search", "")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}")
    elif "play" in command:
        query = command.replace("play", "")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        speak(f"Playing {query} on YouTube")
    elif "remind me" in command:
        speak("What should I remind you about?")
        reminder = listen_command()
        speak("In how many minutes?")
        try:
            minutes = int(listen_command().split()[0])
            set_reminder(reminder, minutes * 60)
            speak(f"Reminder set for {minutes} minutes.")
        except:
            speak("Sorry, I couldn't understand the time.")
    elif "set alarm" in command:
        speak("Tell me the time in HH:MM format.")
        alarm_time = listen_command()
        set_alarm(alarm_time)
        speak(f"Alarm set for {alarm_time}")
    elif "shutdown" in command or "restart" in command or "lock" in command:
        system_control(command)
    elif "how are you" in command:
        speak("I'm ready to help you.")
    elif "thank you" in command:
        speak("You're welcome.")
    elif "exit" in command or "stop" in command:
        speak("Goodbye.")
        exit()
    else:
        speak("Sorry, I don't understand that.")

if __name__ == "__main__":
    speak("Voice assistant is ready.")
    while True:
        command = listen_command()
        if command:
            handle_command(command)    

