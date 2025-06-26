import datetime
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import time
import pyautogui
import random
import ctypes
import subprocess
import pywhatkit

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

contacts = {
    "saif": "+919599236171", 
    "fardeen": "+919773819327", 
    "billu": "+917895991012"
}

def speak(text):
    engine.setProperty('rate', 190)
    engine.say(text)
    engine.runAndWait()

def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
            print("Recognizing...")
            result = recognizer.recognize_google(audio, language='en-US', show_all=True)

            if result and isinstance(result, dict):
                try:
                    text = result["alternative"][0]["transcript"]
                    print("You said:", text)
                    return text.lower()
                except (KeyError, IndexError):
                    print("You said: (could not extract transcript)")
                    return ""
            else:
                print("You said: (speech not recognized clearly)")
                return ""

        except sr.RequestError:
            print("You said: (API/network error)")
            speak("Please check your internet connection.")
            return ""

        except sr.UnknownValueError:
            print("You said: (Unrecognized speech)")
            return ""

        except sr.WaitTimeoutError:
            print("You said: (No speech detected)")
            return ""

def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 15:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hello, I am Jarvis. How can I help you?")

def send_whatsapp_message():
    speak("Who do you want to send a message to?")
    contact_name = take_command()

    if contact_name and contact_name in contacts:
        speak("What is the message?")
        message = take_command()

        if message:
            number = contacts[contact_name]
            speak(f"Sending message to {contact_name}...")

            try:
                pywhatkit.sendwhatmsg_instantly(number, message, wait_time=7, tab_close=True)
                time.sleep(7)
                pyautogui.press("enter")
                speak("Message sent successfully.")
            except Exception as e:
                speak(f"Failed to send message. Error: {str(e)}")
        else:
            speak("I did not get the message. Please try again.")
    else:
        speak("Sorry, I couldn't find that contact.")

def play_music():
    speak("Opening your music playlist.")
    webbrowser.open("https://www.youtube.com/music")

def show_weather():
    speak("Opening weather information.")
    webbrowser.open("https://www.weather.com")

def lock_pc():
    if os.name == 'nt':
        speak("Locking the computer")
        ctypes.windll.user32.LockWorkStation()

def shutdown_pc():
    if os.name == 'nt':
        speak("Shutting down the computer.")
        os.system("shutdown /s /f /t 5")

def take_screenshot():
    speak("Taking a screenshot")
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot saved.")

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "Why was the math book sad? Because it had too many problems."
    ]
    speak(random.choice(jokes))

def main():
    wish_user()
    while True:
        command = take_command()
        if command:
            if 'hello jarvis' in command:
                speak("Hello! How can I help you?")
            elif 'send a message' in command:
                send_whatsapp_message()
            elif 'open youtube' in command:
                webbrowser.open("https://www.youtube.com")
            elif 'what time is it' in command:
                speak(datetime.datetime.now().strftime("%I:%M %p"))
            elif 'open google' in command:
                webbrowser.open("https://www.google.com")
            elif 'play music' in command:
                play_music()
            elif 'show weather' in command:
                show_weather()
            elif 'lock pc' in command:
                lock_pc()
            elif 'shut down' in command:
                shutdown_pc()
            elif 'take a screenshot' in command:
                take_screenshot()
            elif 'tell me a joke' in command:
                tell_joke()
            elif 'exit' in command:
                speak("Goodbye!")
                break
            else:
                speak("I am not sure how to help with that.")
        else:
            time.sleep(2)

if __name__ == "__main__":
    main()
