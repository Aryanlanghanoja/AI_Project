import pandas as pd
import torch
import pickle
import pyttsx3
import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util

# --------- TTS Setup ---------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

# --------- STT Setup ---------
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
        print("Sorry, I couldn't understand your speech.")
        return ""
    except sr.RequestError:
        print("Error with Google Speech Recognition service.")
        return ""

# --------- Load Model/Data ---------
with open("./chatbot_model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
questions = data["questions"]
answers = data["answers"]
question_embeddings = data["embeddings"]

# --------- Main Loop ---------
while True:
    user_input = listen()
    if user_input.lower() in ["exit", "quit", "bye","thanks","thank you"]:
        speak("Goodbye!")
        break

    if user_input.strip() == "":
        continue

    # Encode user question
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    # Find best match using cosine similarity
    cosine_scores = util.cos_sim(user_embedding, question_embeddings)
    best_match_idx = torch.argmax(cosine_scores)

    response = answers[best_match_idx]
    print(f"🤖 Answer: {response}")
    speak(response)
