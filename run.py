# flask imports
from flask import Flask
from flask_bcrypt import Bcrypt
from models import db

import os
from dotenv import load_dotenv

# Initialized flask application
app = Flask(__name__)

load_dotenv()

# Get the Database credentials from environment variables
YOUR_SECRET_KEY = os.getenv('SECRET_KEY')
YOUR_DATABASE_URL = os.getenv('DATABASE_URL')

# Application configuration
app.config['SQLALCHEMY_DATABASE_URI'] = YOUR_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = YOUR_SECRET_KEY

db.init_app(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)
deleted_tokens = set()

from views import *
import admin, user

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9696, debug=True)