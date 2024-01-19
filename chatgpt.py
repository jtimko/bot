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
            print(trigger)
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
    temperature=0.7,
    max_tokens=256,
    top_p=0.9,
    n=2,
    stop=None,
    frequency_penalty=0.9,
    presence_penalty=0.9
    )
    return chat_completion.choices[0].message.content

is_listening_for_question = False

r = sr.Recognizer()
r.energy_threshold = 49.69952687289611
with sr.Microphone(0) as source:
    r.adjust_for_ambient_noise(source, duration=1)
r.listen_in_background(sr.Microphone(0), callback, phrase_time_limit=5)

for _ in range(50):
    time.sleep(0.1)

while True:
    time.sleep(0.1)


# class ChatBot:
#     def __init__(self):
#         load_dotenv()
#         self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
#         self.r = sr.Recognizer()
#         self.r.energy_threshold = 49.69952687289611
#         self.bot_name = "Charlie"
#         self.is_listening_for_question = False

#     def start_bot(self):
#         with sr.Microphone(0) as source:
#             self.r.adjust_for_ambient_noise(source, duration=1)
#         self.r.listen_in_background(sr.Microphone(0), self.callback, phrase_time_limit=5)

#     def ask_chatbot(self, question):
#         chat_completion = self.client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a snarky chatbot that has a crude sense of humor.",
#             },
#             {
#                 "role": "user",
#                 "content": question,
#             }
#         ],
#         model="gpt-3.5-turbo",
#         temperature=0.7,
#         max_tokens=256,
#         top_p=0.9,
#         n=2,
#         stop=None,
#         frequency_penalty=0.9,
#         presence_penalty=0.9
#         )
#         return chat_completion.choices[0].message.content

#     def SpeakText(command):
#         engine = pyttsx3.init()
#         engine.say(command)
#         engine.runAndWait()

#     def callback(self, recognizer, audio):
#         try:
#             if not self.is_listening_for_question:
#                 trigger = recognizer.recognize_google(audio)
#                 print(trigger)
#                 if self.bot_name in trigger.lower():
#                     print("Listening...")
#                     self.is_listening_for_question = True
#             else:
#                 question = recognizer.recognize_google(audio)
#                 question = question.lower()
#                 if len(question) > 0:
#                     self.SpeakText(self.ask_chatbot(question))
#                     self.is_listening_for_question = False

#         except LookupError:
#             print("Could not understand audio")
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))
#         except sr.UnknownValueError:
#             print("unknown error occured")


# bot = ChatBot()
# bot.start_bot()