import pandas as pd
import torch
import pickle
from sentence_transformers import SentenceTransformer

# Load CSVV file
df = pd.read_csv("../dataset/questions.csv")  # Ensure it has 'Question' and 'Answer' columns

# Extract questions and answers
questions = df['Question'].tolist()
answers = df['Answer'].tolist()

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute embeddings for predefined questions
question_embeddings = model.encode(questions, convert_to_tensor=True)

# Save the model, embeddings, and data as a PKL file
with open("chatbot_model.pkl", "wb") as f:
    pickle.dump({"model": model, "questions": questions, "answers": answers, "embeddings": question_embeddings}, f)

print("Model and embeddings saved successfully!")
