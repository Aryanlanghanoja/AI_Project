import pandas as pd
import torch
import pickle
from sentence_transformers import SentenceTransformer, util
import speech_recognition as sr
import pyttsx3

# --------- Speech Engine Setup ---------
engine = pyttsx3.init()
engine.setProperty("rate", 160)  # Speaking speed

def speak(text):
    print("Chatbot:", text)
    engine.say(text)
    engine.runAndWait()

# --------- Listen via Microphone ---------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your question:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand your speech.")
        return ""
    except sr.RequestError:
        speak("There was an issue with the speech recognition service.")
        return ""

# --------- Load Model and Data ---------
with open("ict_chatbot_model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]  # SentenceTransformer model
questions = data["questions"]
answers = data["answers"]
question_embeddings = data["embeddings"]

# --------- Find Best Match ---------
def find_best_match(user_input):
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)
    best_match_index = torch.argmax(similarities).item()
    return answers[best_match_index]

# --------- Voice Chatbot Loop ---------
def voice_chatbot():
    speak("Hello! I am your ICT chatbot. Ask me anything. Say 'exit' to quit.")

    while True:
        user_query = listen()
        if user_query.lower() in ["exit", "quit", "bye", "thank you", "thanks"]:
            speak("Goodbye! Have a great day.")
            break

        if user_query.strip() == "":
            continue

        response = find_best_match(user_query)
        speak(response)

# Run chatbot
voice_chatbot()
