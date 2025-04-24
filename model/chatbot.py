import pandas as pd
import torch
import pickle
from sentence_transformers import SentenceTransformer

# Load CSVV file
df = pd.read_csv("../dataset/questions.csv")  # Ensure it has 'Question' and 'Answer' columns

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
    
# Extract questions and answers
questions = df['Question'].tolist()
answers = df['Answer'].tolist()

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute embeddings for predefined questions
question_embeddings = model.encode(questions, convert_to_tensor=True)

# --------- Main Loop ---------
while True:
    user_input = listen()
    if user_input.lower() in ["exit", "quit", "bye","thanks","thank you"]:
        speak("Goodbye!")
        break

print("Model and embeddings saved successfully!")
