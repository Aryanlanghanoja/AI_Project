from flask import Flask, jsonify, request, render_template  # type: ignore
import server.load_dependencies

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("/index.html")

@app.route("/predict_answer" , methods = ["POST"])
def Response_Question() :
    question = request.form.get("question")
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