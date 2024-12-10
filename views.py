# Admin-Users APIs
import jwt
from flask import request, jsonify
from run import app, bcrypt, deleted_tokens
from models import User
from auth import token_required
from datetime import datetime, timedelta


# Admin-User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Incomplete data!"}), 400
    
    # Find the user
    current_user = User.query.filter_by(email=email).first()

    # Verify user credentials
    if not current_user:
        return jsonify({"message" : "Could not verify!"}), 401
    
    if bcrypt.check_password_hash(current_user.password, data['password']):
        payload = {"id": current_user.id,
                   "is_admin": current_user.is_admin,
                   "exp": datetime.now() + timedelta(hours=1)
                   }
        
        token = jwt.encode(payload=payload, key=app.config['SECRET_KEY'], algorithm="HS256")
       
        return jsonify({"message": "Logged in successully!", "token": token}), 200

    return jsonify({"message": "Login Failed! Check Credientials."}), 401

# Admin-User Logout
@app.route("/logout")
@token_required()
def signout(current_user):
    token = request.headers.get('Authentication')
    deleted_tokens.add(token)
    
    return jsonify({"message": "Log out sucessfully!"}), 200


