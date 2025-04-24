from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS  # Allow frontend to access API

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the QA model
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Sample context
context = """
Thanks to its illustrious past as a princely state, Rajpipla even today has many stately buildings and palaces.
The Vadia Palace of Rajpipla is predominantly Indo-Saracenic with a huge dome, flanked by smaller domes, an umbrella dome and turrets. The massive porticoes at front, rear and side entrances are supported by cusped arches. Arches run the length of the front-elevation and to the rear intricate lattice-work on stone sheltered the princesses from prying eyes.
The Vijay Palace was built largely in European style. It has a classical colonnaded semi-circular portico as the entrance, Corinthian pillars, Gothic arches, European domes and views of the river at the rear.
The Natvar Niwas is another palace property in Rajpipla, which also has rooms to let and is becoming popular for film shoots. The highlight of the Natvar Niwas is the stunning drawing room with a marble fountain and Krishna Lila murals.
"""

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    result = qa_pipeline(question=question, context=context)
    return jsonify({
        "question": question,
        "answer": result['answer'],
        "score": result['score']
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

