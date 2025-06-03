import speech_recognition as sr  # Voice recognition
import webbrowser as wb          # Open websites
import pyttsx3 as py          # type: ignore # Text to speech
import musiclaibrary as ml
import os
import subprocess
import shutil
import glob
from pathlib import Path


recognizer = sr.Recognizer()
engine = py.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_app(command):
    user_folder = str(Path.home())# Get user's home directory (e.g., C:/Users/Om)
    
    # Try opening folders
    folder_keywords = ["downloads", "documents", "desktop", "pictures", "videos", "music"]
    for folder in folder_keywords:
        if folder in command:
            folder_path = os.path.join(user_folder, folder.capitalize())
            if os.path.exists(folder_path):
                os.startfile(folder_path)
                speak(f"Opening {folder}")
                return

    # Try opening known apps in PATH
    app_name = command.replace("open ", "").strip()
    try:
        subprocess.Popen(app_name)
        speak(f"Opening {app_name}")
        return
    except FileNotFoundError:
        pass

    # Try searching for app executables in Program Files
    program_dirs = [
        "C:\\Program Files", 
        "C:\\Program Files (x86)"
    ]
    for dir in program_dirs:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.lower().startswith(app_name.lower()) and file.endswith(".exe"):
                    full_path = os.path.join(root, file)
                    subprocess.Popen(full_path)
                    speak(f"Opening {file}")
                    return

    # Try finding matching files (e.g., "resume")
    for root, dirs, files in os.walk(user_folder):
        for file in files:
            if app_name.lower() in file.lower():
                file_path = os.path.join(root, file)
                os.startfile(file_path)
                speak(f"Opening file {file}")
                return

    speak("Sorry, I couldn't find that application, folder, or file.")
    
def processCommand(c):
    if "open google" in c.lower():
        wb.open("https://google.com")
    elif "open linkedin" in c.lower():
        wb.open("https://linkedin.com")
    elif "open instagram" in c.lower():
        wb.open("https://instagram.com")
    elif "open youtube" in c.lower():
        wb.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        for key in ml.music:
            if key.lower() == song:
                link = ml.music[key]
                wb.open(link)
                break
    else:
        open_app(c)

if __name__ == "__main__":
    speak("Initializing Siri...")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Say 'Siri' to activate:")
                speak("Say 'Siri' to activate:")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                wake_word = recognizer.recognize_google(audio)
                
                if wake_word.lower() == "jarvis":
                    speak("Yes sir, what can I do for you?")
                    print("Listening for your command...")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)
                    print(f"You said: {command}")
                    speak("Ok Sir")
                    processCommand(command)
                   
        except Exception as e:
            print("Error: {0}".format(e))
