# backend/__init__.py

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_DIRECTORY = '/backend/data/uploads'
