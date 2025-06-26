from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("Google_API_Key"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Route for serving the HTML page
@app.route("/")
def home():
    return render_template("index.html")

# API endpoint for handling questions
@app.route("/ask", methods=["POST"])
def ask_gemini():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"response": "Please enter a valid question."}), 400

        response = model.generate_content(question)
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
