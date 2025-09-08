from flask import request, jsonify
from flask_restful import Resource
from models.customer import Customer
from services.customer_service import CustomerService
from middleware.auth_middleware import token_required, admin_required, customer_required

customer_service = CustomerService()

class CustomerResource(Resource):
    @token_required
    def get(self, customer_id):
        """Get a customer by ID"""
        # Check if user is requesting their own profile or has admin rights
        if request.user_role == 'customer' and request.user_id != customer_id and request.user_role != 'admin':
            return {"message": "Unauthorized to access this customer's information"}, 403
            
        customer = customer_service.get_customer_by_id(customer_id)
        if not customer:
            return {"message": "Customer not found"}, 404
        return customer, 200
    
    @token_required
    def put(self, customer_id):
        """Update a customer"""
        # Check if user is updating their own profile or has admin rights
        if request.user_role == 'customer' and request.user_id != customer_id and request.user_role != 'admin':
            return {"message": "Unauthorized to update this customer's information"}, 403
            
        data = request.get_json()
        
        # If not admin, restrict what fields can be updated
        if request.user_role != 'admin':
            allowed_fields = ['name', 'email', 'phone', 'address']
            data = {k: v for k, v in data.items() if k in allowed_fields}
            
        updated = customer_service.update_customer(customer_id, data)
        if not updated:
            return {"message": "Customer not found"}, 404
        return {"message": "Customer updated successfully"}, 200
    
    @admin_required
    def delete(self, customer_id):
        """Delete a customer (admin only)"""
        deleted = customer_service.delete_customer(customer_id)
        if not deleted:
            return {"message": "Customer not found"}, 404
        return {"message": "Customer deleted successfully"}, 200

class CustomerListResource(Resource):
    @admin_required
    def get(self):
        """Get all customers with optional filtering (admin only)"""
        # Get query parameters for filtering
        email = request.args.get('email')
        phone = request.args.get('phone')
        
        customers = customer_service.get_all_customers(email=email, phone=phone)
        return customers, 200
    
    @admin_required
    def post(self):
        """Create a new customer (admin only)"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'address']
        for field in required_fields:
            if field not in data:
                return {"message": f"Missing required field: {field}"}, 400
        
        # Create customer
        customer_id = customer_service.create_customer(data)
        return {"message": "Customer created successfully", "customer_id": customer_id}, 201

class CustomerProfileResource(Resource):
    @customer_required
    def get(self):
        """Get the current customer's profile"""
        customer = customer_service.get_customer_by_id(request.user_id)
        if not customer:
            return {"message": "Customer profile not found"}, 404
        return customer, 200
    
    @customer_required
    def put(self):
        """Update the current customer's profile"""
        data = request.get_json()
        
        # Restrict what fields can be updated
        allowed_fields = ['name', 'email', 'phone', 'address']
        data = {k: v for k, v in data.items() if k in allowed_fields}
            
        updated = customer_service.update_customer(request.user_id, data)
        if not updated:
            return {"message": "Failed to update profile"}, 400
        return {"message": "Profile updated successfully"}, 200
