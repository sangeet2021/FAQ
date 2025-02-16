from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("./api-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load environment variables
load_dotenv()

# Deepseek API endpoint and key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API")

# Function to get response from Deepseek API
def get_deepseek_response(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # Replace with the correct model name
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Fetch predefined FAQs from Firebase
def get_faqs():
    faqs_ref = db.collection('faqs')
    docs = faqs_ref.stream()
    faqs = {doc.to_dict()['question']: doc.to_dict()['answer'] for doc in docs}
    return faqs

# Route to handle user queries
@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')
    faqs = get_faqs()

    # Check if the query matches a predefined FAQ
    if user_query in faqs:
        return jsonify({"response": faqs[user_query]})
    else:
        # Use Deepseek's API for generative responses
        try:
            response = get_deepseek_response(user_query)
            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)