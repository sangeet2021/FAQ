from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)

# Allow requests from http://localhost:5173
CORS(app, resources={r"/ask": {"origins": "http://localhost:5173", "methods": ["POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

print("Deepseek API Key from .env:", os.getenv("DEEPSEEK_API"))

# Initialize Firebase
try:
    cred = credentials.Certificate(os.path.join(os.getcwd(), "static", "api-key2.json"))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully")
except Exception as e:
    print("Firebase initialization error:", str(e))

# Load environment variables
load_dotenv(".env")

# Deepseek API details
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API")

# Function to get response from Deepseek API
def get_deepseek_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
        print("Sending request to Deepseek API:", data)
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        print("Received response from Deepseek API:", response.json())
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Deepseek API error:", str(e))
        return f"Error: {str(e)}"

# Fetch predefined FAQs from Firebase
def get_faqs():
    try:
        faqs_ref = db.collection('faqs')
        docs = faqs_ref.stream()
        faqs = {doc.to_dict()['question']: doc.to_dict()['answer'] for doc in docs}
        return faqs
    except Exception as e:
        print("Firestore error:", str(e))
        return {}

# Route to handle user queries
@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 200

    # Log the incoming request
    print("Received query:", request.json)

    # Handle the POST request
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"error": "Query not provided"}), 400

    faqs = get_faqs()

    # Check if query matches a predefined FAQ
    if user_query in faqs:
        return jsonify({"response": faqs[user_query]})

    # Use Deepseek API for responses if not a predefined FAQ
    try:
        response = get_deepseek_response(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)