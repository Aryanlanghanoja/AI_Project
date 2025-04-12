import json
import pickle
import torch
from sentence_transformers import util  # Import for pytorch_cos_sim

# Global variables
__loaded_model = None
model = None
questions = None
answers = None
question_embeddings = None

def Load_Model():
    global __loaded_model, model, questions, answers, question_embeddings

    print("Loading Saved Model... Start")

    if __loaded_model is None:
        with open("./model/chatbot_model.pkl", "rb") as f:
            __loaded_model = pickle.load(f)
            f.close()

        model = __loaded_model["model"]
        questions = __loaded_model["questions"]
        answers = __loaded_model["answers"]
        question_embeddings = __loaded_model["embeddings"]

    print("Model Loaded Successfully")

def Get_Response(question):
    user_embedding = model.encode(question, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)
    best_match_index = torch.argmax(similarities).item()
    return answers[best_match_index]

if __name__ == "__main__":
    Load_Model()
    # question = "Hello, how can you help me?"  # example
    # print(Get_Response(question))
