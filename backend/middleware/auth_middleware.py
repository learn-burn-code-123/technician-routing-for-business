import os
import jwt
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get JWT secret key
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev')

def token_required(f):
    """Decorator to require JWT token for route access"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Authentication token is missing'}), 401
        
        try:
            # Decode token
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['sub']
            request.user_role = payload.get('role', 'customer')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Authentication token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid authentication token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role for route access"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user_role != 'admin':
            return jsonify({'message': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated

def technician_required(f):
    """Decorator to require technician role for route access"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user_role != 'technician' and request.user_role != 'admin':
            return jsonify({'message': 'Technician privileges required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated

def customer_required(f):
    """Decorator to require customer role for route access"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user_role != 'customer' and request.user_role != 'admin':
            return jsonify({'message': 'Customer privileges required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated
