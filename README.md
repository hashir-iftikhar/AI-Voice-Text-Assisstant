# 🎙️ AI Voice & Text Assistant

A lightweight, dual-mode AI assistant built in Python. Chat with Google's **Gemini 2.5 Flash** model by typing or speaking, get replies read back to you with text-to-speech, and run it either in the terminal or as a local Gradio web app.

## Features

- 💬 **Text Chat (CLI)** — type to chat with Gemini in the terminal
- 🎤 **Voice Chat (CLI)** — speak into your mic, get spoken + printed replies
- 🌐 **Gradio Text UI** — local web interface with a shareable public link
- 🌐 **Gradio Voice UI** — record audio in the browser, get a spoken reply back
- 📝 **Conversation Logging** — full sessions saved to `conversation_log.txt`
- 🔗 **Smart Link Opening** — recognizes phrases like *"open youtube"* or *"search the internet"* and opens the link Gemini returns
- 🗣️ **Text-to-Speech** — replies read aloud via `pyttsx3`
- ✅ **Basic Test Suite** — pytest coverage for core functions

## Tech Stack

| Purpose | Library |
|---|---|
| LLM | `google-generativeai` (Gemini 2.5 Flash) |
| Speech-to-text | `SpeechRecognition` (Google Speech API) |
| Text-to-speech | `pyttsx3` |
| Web UI | `gradio` |
| Config | `python-dotenv` |

## Project Structure

```
.
├── assisstant.py            # Main application
├── requirements.txt         # Python dependencies
├── test_gemini_reply.py     # Test for the Gemini reply function
├── test_speak.py            # Tests for speak() and google()
├── conversation_log.txt     # Saved chat history (generated at runtime)
└── .env                     # Your API key (not committed)
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/<hashir-iftikhar>/<AI Voice & Text Assisstant>.git
cd <AI Voice & Text Assisstant>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
> **Linux users:** `pyttsx3` needs `espeak` installed: `sudo apt install espeak`
> Microphone input via `SpeechRecognition` also requires `PyAudio`, which can need extra system packages (`portaudio19-dev` on Linux, or `pip install pipwin && pipwin install pyaudio` on Windows).

### 3. Add your Gemini API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```
Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).


## Usage

```bash
python assisstant.py
```

You'll see a menu:
```
1. Voice Assistant          -> continuous mic listening + spoken replies
2. Text Chat Bot            -> type messages in the terminal
3. Local Launch Text Chat   -> Gradio web UI (text), with public share link
4. Local Launch Voice Bot   -> Gradio web UI (record mic, get spoken reply)
5. Exit                     -> saves conversation log and quits
```

Say or type **"bye"** / **"goodbye"** at any point to end a session — this saves the conversation log and speaks a goodbye message.

### Example session
*(from `conversation_log.txt`)*
```
You (voice): hello
Bot: Hi there! How can I help you today?
You (voice): i want you to help me with the science project
Bot: Of course! I'd love to help with your science project. What topic are you thinking about, or where should we start?
You (voice): it's about projectile motion
Bot: Great choice! Projectile motion is fascinating. What aspect of it are you focusing on, or what part are you finding tricky?
```

## How It Works

1. Input is captured via microphone (`speech_recognition`) or typed directly.
2. The text is sent to a **persistent Gemini chat session**, which keeps full conversation context turn-to-turn.
3. If the message contains certain keyword combinations (`"search"` + `"internet"` + `"open"`, or `"open"` + `"youtube"` + `"play"`), the assistant treats Gemini's reply as a URL and opens it in the browser.
4. The reply is printed, optionally spoken aloud, and appended to the session log.
5. On exit, the full conversation is appended to `conversation_log.txt`.

## Running Tests

```bash
pytest
```

Covers:
- `gemini_reply()` returns a non-empty response
- `speak()` runs without raising an error
- `google()` opens a URL without raising an error

> ⚠️ These tests make a **live call** to the Gemini API (need a valid `.env` key) and will actually use your speakers / open a browser tab when run.

## Known Limitations

- `text_chat()` does not speak replies aloud — only `voice_chat()` does.
- Link-opening intents rely on simple keyword matching, so phrasing has to closely match the expected patterns.
- The Gradio voice demo (`voice_with_gemini`) records a fixed 10-second window per turn.
- `launch_TB()` runs Gradio with `share=True`, creating a temporary **public** URL — avoid this for sensitive conversations.

## Roadmap

- [ ] Return spoken audio directly in the Gradio voice demo (not just local playback)
- [ ] Replace keyword-based intent matching with more robust parsing
- [ ] Stream Gemini responses for lower latency

## License

MIT — feel free to fork and build on this.

---
Built by Muhammad Hashir Iftikhar
Email muhammadhashiriftikhar@gmail.com
