"""
Voice Assistant (Advanced)
Oasis Infobyte AICTE SIP - Python Programming Track - Task 5

A voice assistant that understands free-form spoken or typed commands and
performs useful actions: greetings, time/date, web search, sending email,
timed reminders, live weather, and general knowledge Q&A.

Works in two input modes:
- Voice mode: uses the microphone via speech_recognition (if available)
- Text mode: type commands instead (automatic fallback if no microphone/
  PyAudio is available, or if the user prefers typing)

See README.md for a full privacy note on what data is processed and how.
"""

import datetime
import json
import os
import re
import smtplib
import threading
import time
import webbrowser
from difflib import SequenceMatcher
from email.mime.text import MIMEText


import requests

# ---------------------------------------------------------------------------
# Configuration - fill these in before running.
# NEVER commit real email credentials or API keys to a public GitHub repo.
# ---------------------------------------------------------------------------

WEATHER_API_KEY = "api key"

EMAIL_ADDRESS = "abeera.voicebot.test@gmail.com"
EMAIL_APP_PASSWORD = "my password"

CUSTOM_COMMANDS_FILE = "custom_commands.json"

# Try to import optional voice libraries. If they're missing or fail to
# load (PyAudio is notoriously tricky to install on some systems), the
# assistant gracefully falls back to typed text input instead of crashing.
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


# ---------------------------------------------------------------------------
# Speech output (falls back to print() if pyttsx3 isn't available)
# ---------------------------------------------------------------------------

_tts_engine = None
if VOICE_AVAILABLE:
    try:
        _tts_engine = pyttsx3.init()
    except Exception:
        _tts_engine = None


def speak(text):
    """Speaks the given text aloud if possible, and always prints it too."""
    print(f"Assistant: {text}")
    if _tts_engine:
        try:
            _tts_engine.say(text)
            _tts_engine.runAndWait()
        except Exception:
            pass  # If speech fails for any reason, printed text is still shown.


# ---------------------------------------------------------------------------
# Input handling: voice (microphone) or typed text
# ---------------------------------------------------------------------------

def listen_voice():
    """
    Captures one spoken command from the microphone and returns it as text.
    Returns None if the speech wasn't understood (caller should ask the
    user to repeat).
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.WaitTimeoutError:
        return None
    except Exception as e:
        print(f"(Microphone error: {e})")
        return None


def get_command(use_voice):
    """Gets one command from the user, via microphone or typed text."""
    if use_voice:
        command = listen_voice()
        while command is None:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            command = listen_voice()
        return command
    else:
        return input("You: ").strip()


# ---------------------------------------------------------------------------
# Natural language intent understanding
#
# Rather than matching a single fixed keyword, each intent has several
# example phrasings. A free-form sentence is compared against ALL example
# phrasings for ALL intents using text similarity, and the best overall
# match is chosen - this lets slightly different wordings (e.g. "what's
# the weather like in Lahore" vs "tell me the weather in Lahore") still
# correctly resolve to the same intent.
# ---------------------------------------------------------------------------

INTENT_EXAMPLES = {
    "greeting": ["hello", "hi", "hey there", "good morning", "greetings"],
    "time": ["what time is it", "tell me the time", "current time"],
    "date": ["what is the date today", "tell me today's date", "what day is it"],
    "web_search": ["search for", "look up", "google", "search the web for"],
    "send_email": ["send an email", "email someone", "compose an email"],
    "set_reminder": ["set a reminder", "remind me", "set a timer", "wake me up in"],
    "weather": ["what's the weather", "tell me the weather", "weather in", "how hot is it"],
    "question": ["what is", "who is", "where is", "why is", "how does", "tell me about"],
    "add_command": ["add a custom command", "teach you a new command"],
    "exit": ["exit", "quit", "stop", "goodbye", "that's all"],
}


def detect_intent(text):
    """
    Compares the input text against example phrasings for every intent
    and returns the intent with the highest similarity score, along with
    that score (0 to 1).
    """
    text_lower = text.lower().strip()
    best_intent = None
    best_score = 0.0

    for intent, examples in INTENT_EXAMPLES.items():
        for example in examples:
            score = SequenceMatcher(None, text_lower, example).ratio()
            # Also boost the score heavily if the example phrase literally
            # appears as a substring, since that's a very strong signal
            # even if overall sentence length differs a lot.
            if example in text_lower:
                score = max(score, 0.85)
            if score > best_score:
                best_score = score
                best_intent = intent

    return best_intent, best_score


# ---------------------------------------------------------------------------
# Feature: time and date
# ---------------------------------------------------------------------------

def handle_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}.")


def handle_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {today}.")


# ---------------------------------------------------------------------------
# Feature: web search
# ---------------------------------------------------------------------------

def handle_web_search(command_text):
    # Remove the trigger phrase itself to get just the search topic
    topic = re.sub(
        r"(search for|look up|google|search the web for)", "", command_text, flags=re.IGNORECASE
    ).strip()
    if not topic:
        speak("What would you like me to search for?")
        topic = input("Search topic: ").strip()
    if topic:
        speak(f"Searching the web for {topic}.")
        webbrowser.open(f"https://www.google.com/search?q={topic}")
    else:
        speak("I didn't get a topic to search for.")


# ---------------------------------------------------------------------------
# Feature: send email
# ---------------------------------------------------------------------------

def handle_send_email():
    if EMAIL_ADDRESS == "your_dummy_account@gmail.com" or "YOUR_16" in EMAIL_APP_PASSWORD:
        speak("Email isn't set up yet. Please add your email credentials in the code first.")
        return

    speak("Who would you like to email? Please type their email address.")
    to_address = input("Recipient email: ").strip()
    speak("What should the subject be?")
    subject = input("Subject: ").strip()
    speak("What should the email say?")
    body = input("Message: ").strip()

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_address

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Sorry, I couldn't send the email. Error: {e}")


# ---------------------------------------------------------------------------
# Feature: timed reminder
# ---------------------------------------------------------------------------

def handle_set_reminder():
    speak("How many minutes from now should I remind you?")
    try:
        minutes = float(input("Minutes: ").strip())
    except ValueError:
        speak("That didn't look like a number. Reminder cancelled.")
        return

    speak("What should the reminder say?")
    message = input("Reminder message: ").strip()

    def alert():
        print("\n\a--- REMINDER ---")  # \a triggers a terminal bell sound
        speak(f"Reminder: {message}")

    threading.Timer(minutes * 60, alert).start()
    speak(f"Okay, I'll remind you about '{message}' in {minutes} minutes.")


# ---------------------------------------------------------------------------
# Feature: live weather (reuses the same OpenWeatherMap API as Task 4)
# ---------------------------------------------------------------------------

def handle_weather(command_text):
    match = re.search(r"(?:weather in|weather for)\s+([a-zA-Z\s]+)", command_text, re.IGNORECASE)
    if match:
        city = match.group(1).strip()
        # Strip trailing time words that aren't part of the city name
        city = re.sub(r"\s+(today|now|right now|currently)$", "", city, flags=re.IGNORECASE).strip()
    else:
        speak("Which city's weather would you like to know?")
        city = input("City: ").strip()

    if WEATHER_API_KEY == "YOUR_OPENWEATHERMAP_API_KEY_HERE":
        speak("Weather isn't set up yet. Please add your OpenWeatherMap API key in the code first.")
        return

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"},
            timeout=10,
        )
        if response.status_code == 404:
            speak(f"I couldn't find weather data for {city}.")
            return
        if response.status_code == 401:
            speak("The weather API key seems invalid. New keys can take up to 2 hours to activate.")
            return
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        speak(f"The weather in {city} is currently {description} at {temp:.1f} degrees Celsius.")
    except requests.exceptions.RequestException:
        speak("I couldn't reach the weather service. Please check your internet connection.")


# ---------------------------------------------------------------------------
# Feature: general knowledge Q&A (uses Wikipedia's free summary API,
# no API key required)
# ---------------------------------------------------------------------------

def handle_question(command_text):
    # Strip common question words to get a cleaner search topic
    topic = re.sub(
        r"^(what is|what's|who is|where is|why is|how does|tell me about)\s+",
        "", command_text, flags=re.IGNORECASE
    ).strip().rstrip("?")

    if not topic:
        speak("What would you like to know about?")
        topic = input("Topic: ").strip()

    try:
        response = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}",
            timeout=10,
        )
        if response.status_code == 404:
            speak(f"I couldn't find any information about {topic}.")
            return
        response.raise_for_status()
        data = response.json()
        extract = data.get("extract", "")
        if extract:
            speak(extract)
        else:
            speak(f"I found a page for {topic}, but no summary was available.")
    except requests.exceptions.RequestException:
        speak("I couldn't reach the knowledge service. Please check your internet connection.")


# ---------------------------------------------------------------------------
# Feature: custom commands via config file
# ---------------------------------------------------------------------------

def load_custom_commands():
    if os.path.exists(CUSTOM_COMMANDS_FILE):
        with open(CUSTOM_COMMANDS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_custom_commands(commands):
    with open(CUSTOM_COMMANDS_FILE, "w") as f:
        json.dump(commands, f, indent=2)


def handle_add_command(custom_commands):
    speak("What phrase should trigger this new command?")
    trigger = input("Trigger phrase: ").strip().lower()
    speak("What should I say when that phrase is used?")
    response = input("Response: ").strip()
    custom_commands[trigger] = response
    save_custom_commands(custom_commands)
    speak(f"Got it. When you say '{trigger}', I'll respond with that message.")


def check_custom_commands(command_text, custom_commands):
    """Returns a matching custom response if the command text closely matches
    a saved custom trigger phrase, otherwise None."""
    text_lower = command_text.lower().strip()
    for trigger, response in custom_commands.items():
        if trigger in text_lower or SequenceMatcher(None, text_lower, trigger).ratio() > 0.8:
            return response
    return None


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def choose_input_mode():
    if not VOICE_AVAILABLE:
        print("(Voice libraries not available - using text input mode.)")
        return False

    choice = input("Use voice input? (yes/no): ").strip().lower()
    return choice in ("yes", "y")


def main():
    print("=== Voice Assistant (Advanced) ===")
    print("Say or type 'exit' at any time to quit.\n")

    use_voice = choose_input_mode()
    custom_commands = load_custom_commands()

    speak("Hello! How can I help you today?")

    while True:
        command_text = get_command(use_voice)
        if not command_text:
            continue

        print(f"You said: {command_text}")

        # Custom commands are checked first, so users can override/extend behavior
        custom_response = check_custom_commands(command_text, custom_commands)
        if custom_response:
            speak(custom_response)
            continue

        intent, score = detect_intent(command_text)

        if score < 0.45:
            speak("I'm not sure I understood that. Could you rephrase it?")
            continue

        if intent == "greeting":
            speak("Hello! Nice to hear from you.")
        elif intent == "time":
            handle_time()
        elif intent == "date":
            handle_date()
        elif intent == "web_search":
            handle_web_search(command_text)
        elif intent == "send_email":
            handle_send_email()
        elif intent == "set_reminder":
            handle_set_reminder()
        elif intent == "weather":
            handle_weather(command_text)
        elif intent == "question":
            handle_question(command_text)
        elif intent == "add_command":
            handle_add_command(custom_commands)
        elif intent == "exit":
            speak("Goodbye! Have a great day.")
            break


if __name__ == "__main__":
    main()
