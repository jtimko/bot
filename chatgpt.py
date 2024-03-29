from openai import OpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr
import time
import pyttsx3
import pygame
import threading

load_dotenv()

class ChatBot:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.r = sr.Recognizer()
        self.r.energy_threshold = 49.69952687289611
        self.bot_name = "charlie"
        self.is_listening_for_question = False
        self.is_speaking = False
        self.is_showing_text = False
        self.history = [{
                "role": "system",
                "content": "You are a snarky chatbot that has a crude sense of humor.",
            }]
        self.microphone_index = 0

    def start_bot(self):
        with sr.Microphone(self.microphone_index) as source:
            self.r.adjust_for_ambient_noise(source, duration=1)
        self.r.listen_in_background(sr.Microphone(self.microphone_index), self.callback, phrase_time_limit=5)

    def ask_chatbot(self):
        chat_completion = self.client.chat.completions.create(
        messages=self.history,
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=256,
        top_p=0.9,
        n=2,
        stop=None,
        frequency_penalty=0.9,
        presence_penalty=0.9
        )
        self.history.append({"role": "assistant", "content": chat_completion.choices[0].message.content})
        return chat_completion.choices[0].message.content

    def speak_text(self, command):
        engine = pyttsx3.init()
        self.is_speaking = True
        engine.say(command)
        engine.runAndWait()
        self.is_speaking = False

    def callback(self, recognizer, audio):
        try:
            if not self.is_listening_for_question:
                trigger = recognizer.recognize_google(audio)
                print(trigger)
                if self.bot_name in trigger.lower():
                    print("Listening...")
                    self.is_listening_for_question = True
                if "clear" in trigger.lower():
                    self.is_showing_text = False
            else:
                question = recognizer.recognize_google(audio)
                question = question.lower()
                if len(question) > 0:
                    if "show" in question.lower():
                        self.is_showing_text = True
                    self.history.append({"role": "user", "content": question})
                    self.speak_text(self.ask_chatbot())
                    self.is_listening_for_question = False

        except LookupError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")

# Clean up this function
def pygame_thread(bot):
    pygame.init()
    height = 800
    width = 480
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    count = 0
    start_angle = 3.14
    end_angle = 3.14 * 2

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            time.sleep(.5)
            count += 1
            screen.fill("purple")
            print("show text", bot.is_showing_text)
            if bot.is_showing_text:
                font = pygame.font.Font(None, 32)
                text = font.render(bot.history[-1]["content"], True, "white", "purple")
                textRect = text.get_rect()
                textRect.center = (240, 190)
                screen.blit(text, textRect)
            else:
                if count % 10 == 0:
                    pygame.draw.arc(screen, "black", (190, 190, 20, 20), start_angle, end_angle, 1)
                    pygame.draw.arc(screen, "black", (270, 190, 20, 20), start_angle, end_angle, 1)
                else:
                    pygame.draw.circle(screen, "black", (200, 200), 10)
                    pygame.draw.circle(screen, "black", (280, 200), 10)

                if bot.is_listening_for_question:
                    font = pygame.font.Font(None, 32)
                    text = font.render('?', True, "white", "purple")
                    textRect = text.get_rect()
                    textRect.center = (310, 190)
                    screen.blit(text, textRect)
                
                if bot.is_speaking:
                    if count % 2 == 0:
                        pygame.draw.circle(screen, "black", (240, 290), 60)
                        pygame.draw.rect(screen, "purple", (240 - 100, 290 - 60, 2*100, 60), 100)
                    else:
                        pygame.draw.arc(screen, "black", (170, 200, 150, 150), 3.14, 3.14 * 2, 1)
                else:
                    pygame.draw.arc(screen, "black", (170, 200, 150, 150), 3.14, 3.14 * 2, 1)

            pygame.display.flip()
            clock.tick(40)
    except KeyboardInterrupt:
        print("Program stopped manually")

def chatbot_thread(bot):
    bot.start_bot()

bot = ChatBot()
t1 = threading.Thread(target=pygame_thread, args=(bot,))
t2 = threading.Thread(target=chatbot_thread, args=(bot,))
t1.start()
t2.start()
t1.join()