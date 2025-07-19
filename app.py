from flask import Flask, jsonify, request, render_template  # type: ignore
import server.load_dependencies

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict_answer" , methods = ["POST"])
def Response_Question() :
    print(request)
    question = request.form.get("question")
    if not question:
        return jsonify({
            "error": "Question field is required",
            "answer": None
        }), 400
        
    answer = server.load_dependencies.Get_Response(question)
    response = jsonify(
        {
            "answer" : answer
        }   
    )

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction....")
    server.load_dependencies.Load_Model()
    app.run()