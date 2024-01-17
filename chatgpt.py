from openai import OpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr
import time
import pyttsx3

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def callback(recognizer, audio):
    global is_listening_for_question

    try:
        if not is_listening_for_question:
            trigger = recognizer.recognize_google(audio)
            if "charlie" in trigger.lower():
                print("Listening...")
                is_listening_for_question = True
        else:
            question = recognizer.recognize_google(audio)
            question = question.lower()
            if len(question) > 0:
                SpeakText(ask_chatbot(question))
                is_listening_for_question = False

    except LookupError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occured")


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def ask_chatbot(question):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a snarky chatbot that has a crude sense of humor.",
        },
        {
            "role": "user",
            "content": question,
        }
    ],
    model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content

is_listening_for_question = False

r = sr.Recognizer()
with sr.Microphone(0) as source:
    r.adjust_for_ambient_noise(source, duration=1)
r.listen_in_background(sr.Microphone(0), callback)

while True:
    time.sleep(0.1)
