from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from services.user_service import UserService
from services.technician_service import TechnicianService
from services.customer_service import CustomerService
from utils.password_utils import verify_password
import datetime
import os

user_service = UserService()
technician_service = TechnicianService()
customer_service = CustomerService()

# Get JWT settings from environment
JWT_ACCESS_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))  # 24 hours
JWT_REFRESH_EXPIRES = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000))  # 30 days

class LoginResource(Resource):
    def post(self):
        """Login a user"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return {"message": f"Missing required field: {field}"}, 400
        
        # Get user by email
        user = user_service.get_user_by_email(data['email'])
        if not user:
            return {"message": "Invalid credentials"}, 401
        
        # Verify password
        if not verify_password(data['password'], user['password_hash']):
            return {"message": "Invalid credentials"}, 401
        
        # Get additional user info based on role
        additional_info = {}
        if user['role'] == 'technician' and user.get('technician_id'):
            technician = technician_service.get_technician_by_id(user['technician_id'])
            if technician:
                additional_info = {
                    'technician_id': user['technician_id'],
                    'status': technician.get('status', 'available')
                }
        elif user['role'] == 'customer' and user.get('customer_id'):
            customer = customer_service.get_customer_by_id(user['customer_id'])
            if customer:
                additional_info = {
                    'customer_id': user['customer_id'],
                    'service_tier': customer.get('service_tier', 'standard')
                }
        
        # Create tokens with claims
        access_token = create_access_token(
            identity=str(user['_id']),
            additional_claims={
                'role': user['role'],
                **additional_info
            }
        )
        
        refresh_token = create_refresh_token(
            identity=str(user['_id']),
            additional_claims={
                'role': user['role']
            }
        )
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": JWT_ACCESS_EXPIRES,
            "user": {
                "id": str(user['_id']),
                "name": user['name'],
                "email": user['email'],
                "role": user['role'],
                **additional_info
            }
        }, 200

class RegisterResource(Resource):
    def post(self):
        """Register a new user"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return {"message": f"Missing required field: {field}"}, 400
        
        # Validate role
        valid_roles = ['customer', 'technician', 'admin']
        if data['role'] not in valid_roles:
            return {"message": f"Invalid role. Must be one of: {', '.join(valid_roles)}"}, 400
        
        # Check if user already exists
        existing_user = user_service.get_user_by_email(data['email'])
        if existing_user:
            return {"message": "User with this email already exists"}, 409
        
        # Create user
        user_id = user_service.create_user(data)
        
        return {"message": "User registered successfully", "user_id": user_id}, 201

class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        # Get user identity from refresh token
        current_user_id = get_jwt_identity()
        
        # Get claims from refresh token
        claims = get_jwt()
        
        # Get user from database to ensure they still exist and get current role
        user = user_service.get_user_by_id(current_user_id)
        if not user:
            return {"message": "User not found"}, 404
        
        # Create new access token
        access_token = create_access_token(
            identity=current_user_id,
            additional_claims={
                'role': user['role'],
                # Add any other claims needed
            }
        )
        
        return {
            "access_token": access_token,
            "expires_in": JWT_ACCESS_EXPIRES
        }, 200
