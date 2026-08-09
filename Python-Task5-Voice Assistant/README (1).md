# Voice Assistant (Advanced)

**Oasis Infobyte AICTE SIP — Python Programming Track — Task 5**

## What This Project Does

A Python voice assistant that understands free-form spoken or typed
commands and performs useful actions: greetings, telling the time and
date, searching the web, sending emails, setting timed reminders, reading
out live weather, and answering general knowledge questions.

## Features

- **Voice or text input** — uses your microphone via `speech_recognition`
  if available, and automatically falls back to typed text input if
  voice libraries aren't installed (so it always works)
- **Text-to-speech output** — spoken responses via `pyttsx3`, with printed
  text as a backup
- **Natural language understanding** — recognizes intent from differently
  worded free-form sentences (e.g. "what's the weather in Lahore" and
  "tell me the weather for Lahore" both work), not just one fixed keyword,
  using text-similarity matching against multiple example phrasings per
  intent
- **Greetings** — responds to hello/hi/good morning etc.
- **Time & date** — tells the current time and today's date on request
- **Web search** — opens a browser search for any topic you mention
- **Send email** — sends a real email via Gmail (using an App Password,
  not your real password) to any recipient you specify
- **Timed reminders** — set a reminder in X minutes that triggers an
  audible alert (terminal bell + spoken message) when it's due
- **Live weather** — fetches real-time weather for any city using the
  OpenWeatherMap API
- **General knowledge Q&A** — answers "what is/who is/tell me about"
  questions using Wikipedia's free summary API
- **Custom commands** — add your own trigger phrase + response, saved to
  a `custom_commands.json` config file, reusable across sessions
- **Graceful error handling** — if voice input isn't understood, it asks
  you to repeat instead of crashing; network/API failures show friendly
  messages instead of raw errors

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   (If `pyaudio` fails to install, that's okay — the assistant will still
   run fully in text mode. See the Troubleshooting section below.)

2. Open `voice_assistant.py` and fill in your credentials near the top:
   ```python
   WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY_HERE"
   EMAIL_ADDRESS = "your_dummy_account@gmail.com"
   EMAIL_APP_PASSWORD = "YOUR_16_CHARACTER_APP_PASSWORD_HERE"
   ```
   - Get a free weather API key at **openweathermap.org**
   - For email, use a **dummy/test Gmail account** (not your personal one),
     with 2-Step Verification enabled, and generate an **App Password** at
     **myaccount.google.com/apppasswords** — never use your real Gmail
     password here

3. Run it:
   ```
   python voice_assistant.py
   ```

4. Choose voice or text input mode when prompted, then start talking or
   typing commands like:
   - "Hello"
   - "What time is it?"
   - "Search for machine learning basics"
   - "What's the weather in Lahore?"
   - "Who is Marie Curie?"
   - "Remind me in 2 minutes to check the oven"
   - "Send an email"
   - "Exit"

## Privacy Note — What Data Is Processed and How

This project is transparent about what happens to your data:

- **Voice audio**: If you use voice mode, your spoken audio is sent to
  Google's speech recognition service (via the `speech_recognition`
  library's `recognize_google` function) to convert it to text. This
  happens over the internet and is subject to Google's own privacy
  policy. No audio is stored locally or by this program.
- **Typed commands**: Processed entirely locally on your machine; not
  sent anywhere except the specific feature you triggered (e.g. a
  weather request only sends the city name to OpenWeatherMap).
- **Email feature**: Your dummy account's email address and App Password
  are stored in plain text directly in `voice_assistant.py` on your own
  computer. They are only ever sent to Google's SMTP server to send the
  email you compose. **Never commit real credentials to a public GitHub
  repository** — use a dummy/test account for this project.
- **Weather requests**: Only the city name you ask about is sent to the
  OpenWeatherMap API.
- **Q&A requests**: Only your question's topic is sent to Wikipedia's
  public summary API.
- **Custom commands**: Saved locally in `custom_commands.json` on your
  own machine; never transmitted anywhere.

## Troubleshooting

**"speech_recognition" or "pyaudio" won't install:**
This is common, especially on Windows, since PyAudio needs system-level
build tools. The assistant is designed to work perfectly fine without
them — it will automatically use typed text input instead. You can still
complete every feature this way.

**"Invalid API key" for weather:**
New OpenWeatherMap keys can take up to 2 hours to activate after signup.

**Email fails to send:**
Double-check you're using an **App Password**, not your regular Gmail
password, and that 2-Step Verification is enabled on that account.

## Technologies Used

- Python 3
- `speech_recognition` + `pyttsx3` (optional voice I/O)
- `requests` (OpenWeatherMap + Wikipedia APIs)
- `smtplib` (built-in, for sending email)
- `difflib` (built-in, for intent similarity matching)
- `threading` (built-in, for timed reminders)
- `json` (built-in, for custom commands config)

## What I Learned

This was the most complex task in the internship. Building it helped me
practice combining multiple real APIs into one program, designing a
simple but effective natural language matching approach without heavy
NLP libraries, handling optional dependencies gracefully so the program
never crashes even if some libraries aren't installed, and thinking
carefully about privacy and credential security when handling email
sending.
