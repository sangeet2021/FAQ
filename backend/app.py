from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)

# Allow requests from http://localhost:5173
CORS(app, resources={r"/ask": {"origins": "http://localhost:5173"}})

# Load environment variables
load_dotenv(".env")

# Initialize Firebase
try:
    cred = credentials.Certificate(os.path.join(os.getcwd(), "static", "api-key2.json"))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully")
except Exception as e:
    print("Firebase initialization error:", str(e))

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API")

# Function to get response from OpenAI API
def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        print("Received response from OpenAI API:", response)
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("OpenAI API error:", str(e))
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
@app.route('/ask', methods=['POST'])
def ask():
    # Log the incoming request
    print("Received query:", request.json)
    
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"error": "Query not provided"}), 400

    faqs = get_faqs()
    
    # Check if query matches a predefined FAQ
    if user_query in faqs:
        return jsonify({"response": faqs[user_query]})

    # Use OpenAI API for responses if not a predefined FAQ
    try:
        response = get_openai_response(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
