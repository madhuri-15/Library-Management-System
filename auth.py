import jwt
from functools import wraps

from flask import request, jsonify
from models import User
from run import app, deleted_tokens


def token_required(admin_only=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*arg, **kwarg):
            token = request.headers.get('Authentication')
            if not token:
                return jsonify({"message": "Token is missing!"}), 401
            
            try:
                if token in deleted_tokens:
                    return jsonify({"message": "Invalid Token!"}), 401
                
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                user = User.query.get(payload["id"])
                
                if not user or (admin_only and not user.is_admin):
                    return jsonify({"message": "Unauthorized!"}), 403
                
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired!"}), 401
            
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid Token!"}), 401
            
            return f(user, *arg, **kwarg)
        
        return wrapper
    
    return decorator