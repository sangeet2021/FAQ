from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore
import requests
import os
from dotenv import load_dotenv
import deepseek

app = Flask(__name__)

#Firebase

load_dotenv();

# Deepseek API endpoint and key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API")