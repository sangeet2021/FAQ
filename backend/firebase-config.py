import os
from dotenv import load_dotenv

load_dotenv()

firebaseConfig = {
  "apiKey": os.getenv("FIREBASE_API"),
  "authDomain": "faq-bot-23f82.firebaseapp.com",
  "projectId": "faq-bot-23f82",
  "storageBucket": "faq-bot-23f82.firebasestorage.app",
  "messagingSenderId": "942099535091",
  "appId": "1:942099535091:web:2d372d75d5d831f8da1386",
  "measurementId": "G-KKNZ91DRBH"
};