from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore
import requests

app = Flask(__name__)

#Firebase

# Deepseek API endpoint and key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
