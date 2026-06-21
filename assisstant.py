import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import sys
import os
import webbrowser
import dotenv
import gradio as gr

dotenv.load_dotenv()


# GEMINI API SETUP

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Create a persistent chat session
chat = model.start_chat(history=[
    {"role": "user", "parts": "You are a helpful, cheerful assistant for a student. Keep answers short and precise. Do not use any emojis. and when asked to open something om the internet reply with only the link nothing else"}
])


# SPEECH + TTS

r = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty("rate", 150)


# STATE

conversation_log = []


# UTIL

def speak(text):
    local_engine = pyttsx3.init()
    local_engine.setProperty("rate", 150)
    local_engine.say(text)
    local_engine.runAndWait()
    

   
def save_log(filename="conversation_log.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        for line in conversation_log:
            f.write(line + "\n")
    print(f"Conversation saved to {filename}")
    speak("Conversation log saved.")


# GEMINI CALL 

def gemini_reply(user_text):                                                                                                                
    try:
        response = chat.send_message(user_text)
        reply = response.text.strip()
    except Exception as e:
        print("Gemini API Error:", e)
        reply = "Sorry, I couldn't reach the server."
    return reply


# VOICE ASSISTANT

def voice_chat():
    while True:
        with mic as source:
            print("Say something...")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio).lower().strip()
            print("You said:", text)
            conversation_log.append(f"You (voice): {text}")

            if "bye" in text or "goodbye" in text:
                speak("Goodbye! Talk to you later.")
                save_log()
                sys.exit()
            if "search" in text and "internet" in text and "open" in text:
                rep = gemini_reply(text)
                google(rep)
                print(rep)
            if "open" in text and "youtube" in text and "play" in text:
                rep1 = gemini_reply(text)
                google(rep1)
                print(rep1)

            reply = gemini_reply(text)
            print("Bot:", reply)
            speak(reply)
            conversation_log.append(f"Bot: {reply}")

        except sr.UnknownValueError:
            print("Speech not recognized.")
        except sr.RequestError as e:
            print("Google Speech error:", e)


# CHAT BOT (TEXT MODE)

def text_chat():
    while True:
        text = input("You: ").strip()
        if not text:
            continue
        conversation_log.append(f"You (text): {text}")

        if "bye" in text or "goodbye" in text:
        
            speak("Goodbye! Talk to you later.")
            save_log()
            sys.exit()
        if "search" in text and "internet" in text and "open" in text:
            rep = gemini_reply(text)
            google(rep)
            print(rep)
        if "open" in text and "youtube" in text and "play" in text:
            rep1 = gemini_reply(text)
            google(rep1)
            print(rep1)

        reply = gemini_reply(text)
        print("Bot:", reply)
        
        conversation_log.append(f"Bot: {reply}")

# GOOGLE SEARCH

def google(query):
    webbrowser.open(query)

    
# LOCAL LAUNCH TB
def launch_TB():
    demo = gr.Interface(
        fn=gemini_reply,
        inputs=gr.Textbox(label="Enter your message"),
        outputs=gr.Textbox(label="Response"),
        title="AI BOT"
        
     )
    demo.launch(share=True)

# LOCAL LAUNCH VB
def voice_with_gemini(audio):
    
    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio) as source:
            
            audio_data = recognizer.record(source, duration=10)

        text = recognizer.recognize_google(audio_data)

        reply = gemini_reply(text)
        speak(reply)

        conversation_log.append(f"You (voice): {text}")
        conversation_log.append(f"Bot: {reply}")

        return "\n".join(conversation_log)

    except sr.UnknownValueError:
        return "Speech not recognized."
    except sr.RequestError as e:
        return f"Speech service error: {e}"



def launch_VB():
    
    demo = gr.Interface(
    fn=voice_with_gemini,
    inputs=gr.Audio(sources=["microphone"], type="filepath"),
    outputs=gr.Textbox(label="Conversation"),
    title="Voice Assistant with Gemini")
    demo.launch()
# MAIN

if __name__ == "__main__":
    while True:
        print("Choose mode:")
        print("1. Voice Assistant")
        print("2. Text Chat Bot")
        print("3. Local Launch Text chat")
        print("4. Local Launch Voice Bot")
        print("5. Exit")

        mode = input("Enter choice: ").strip()

        if mode == "1":
            voice_chat()
        elif mode == "2":
            text_chat()
        elif mode =="3":
            launch_TB()
        elif mode =="4":
            launch_VB()
        elif mode == "5":
            print("Goodbye!")
            save_log()
            sys.exit()
        else:
            print("Invalid choice. Try again.")



