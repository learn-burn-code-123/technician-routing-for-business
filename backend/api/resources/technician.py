from flask import request, jsonify
from flask_restful import Resource
from models.technician import Technician
from services.technician_service import TechnicianService
from middleware.auth_middleware import token_required, admin_required, technician_required

technician_service = TechnicianService()

class TechnicianResource(Resource):
    @token_required
    def get(self, technician_id):
        """Get a technician by ID"""
        # Check if user is requesting their own profile or has admin rights
        if request.user_role == 'technician' and request.user_id != technician_id and request.user_role != 'admin':
            return {"message": "Unauthorized to access this technician's information"}, 403
            
        technician = technician_service.get_technician_by_id(technician_id)
        if not technician:
            return {"message": "Technician not found"}, 404
        return technician, 200
    
    @admin_required
    def put(self, technician_id):
        """Update a technician (admin only)"""
        data = request.get_json()
        updated = technician_service.update_technician(technician_id, data)
        if not updated:
            return {"message": "Technician not found"}, 404
        return {"message": "Technician updated successfully"}, 200
    
    @admin_required
    def delete(self, technician_id):
        """Delete a technician (admin only)"""
        deleted = technician_service.delete_technician(technician_id)
        if not deleted:
            return {"message": "Technician not found"}, 404
        return {"message": "Technician deleted successfully"}, 200

class TechnicianListResource(Resource):
    @token_required
    def get(self):
        """Get all technicians"""
        # Get query parameters for filtering
        status = request.args.get('status')
        skill = request.args.get('skill')
        
        # Regular users can only see basic technician info
        if request.user_role == 'customer':
            technicians = technician_service.get_all_technicians(status=status, skill=skill, basic_info_only=True)
        else:
            technicians = technician_service.get_all_technicians(status=status, skill=skill)
            
        return technicians, 200
    
    @admin_required
    def post(self):
        """Create a new technician (admin only)"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'skills']
        for field in required_fields:
            if field not in data:
                return {"message": f"Missing required field: {field}"}, 400
        
        # Create technician
        technician_id = technician_service.create_technician(data)
        return {"message": "Technician created successfully", "technician_id": technician_id}, 201

class TechnicianProfileResource(Resource):
    @technician_required
    def get(self):
        """Get the current technician's profile"""
        technician = technician_service.get_technician_by_id(request.user_id)
        if not technician:
            return {"message": "Technician profile not found"}, 404
        return technician, 200
    
    @technician_required
    def put(self):
        """Update the current technician's profile"""
        data = request.get_json()
        
        # Prevent changing sensitive fields
        if 'status' in data or 'skills' in data:
            return {"message": "Cannot update status or skills directly"}, 403
            
        updated = technician_service.update_technician(request.user_id, data)
        if not updated:
            return {"message": "Failed to update profile"}, 400
        return {"message": "Profile updated successfully"}, 200

class TechnicianLocationResource(Resource):
    @technician_required
    def put(self):
        """Update the current technician's location"""
        data = request.get_json()
        
        if 'location' not in data:
            return {"message": "Missing location data"}, 400
            
        updated = technician_service.update_technician_location(request.user_id, data['location'])
        if not updated:
            return {"message": "Failed to update location"}, 400
        return {"message": "Location updated successfully"}, 200

class TechnicianStatusResource(Resource):
    @technician_required
    def put(self):
        """Update the current technician's status"""
        data = request.get_json()
        
        if 'status' not in data:
            return {"message": "Missing status data"}, 400
            
        if data['status'] not in ['available', 'busy', 'off-duty']:
            return {"message": "Invalid status value"}, 400
            
        updated = technician_service.update_technician_status(request.user_id, data['status'])
        if not updated:
            return {"message": "Failed to update status"}, 400
        return {"message": "Status updated successfully"}, 200
