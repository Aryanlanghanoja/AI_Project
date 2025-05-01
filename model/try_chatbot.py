import torch
import pickle
from sentence_transformers import SentenceTransformer, util

# Load the trained model from the pickle file
with open("ict_chatbot_model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
questions = data["questions"]
answers = data["answers"]
question_embeddings = data["embeddings"]


# Define function to find best match
def find_best_match(user_input):
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)
    best_match_index = torch.argmax(similarities).item()
    return answers[best_match_index]


# Example usage
def chatbot():
    print("Chatbot: Ask me anything! Type 'exit' to quit.")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        response = find_best_match(user_query)
        print("Chatbot:", response)


# Run chatbot
chatbot()

