from flask import request, jsonify
from flask_restful import Resource
from models.job import Job
from services.job_service import JobService
from services.routing_service import RoutingService
from middleware.auth_middleware import token_required, admin_required, technician_required, customer_required

job_service = JobService()
routing_service = RoutingService()

class JobResource(Resource):
    @token_required
    def get(self, job_id):
        """Get a job by ID"""
        job = job_service.get_job_by_id(job_id)
        if not job:
            return {"message": "Job not found"}, 404
            
        # Check authorization - customers can only see their own jobs
        if request.user_role == 'customer' and job.get('customer_id') != request.user_id:
            return {"message": "Unauthorized to access this job"}, 403
            
        return job, 200
    
    @token_required
    def put(self, job_id):
        """Update a job"""
        data = request.get_json()
        
        # Get existing job to check permissions
        job = job_service.get_job_by_id(job_id)
        if not job:
            return {"message": "Job not found"}, 404
            
        # Check authorization
        if request.user_role == 'customer' and job.get('customer_id') != request.user_id:
            return {"message": "Unauthorized to update this job"}, 403
        elif request.user_role == 'technician' and job.get('technician_id') != request.user_id:
            return {"message": "Unauthorized to update this job"}, 403
            
        # Restrict what fields can be updated based on role
        if request.user_role == 'customer':
            # Customers can only update notes
            allowed_fields = ['notes']
            data = {k: v for k, v in data.items() if k in allowed_fields}
        elif request.user_role == 'technician':
            # Technicians can update status and notes
            allowed_fields = ['status', 'notes', 'actual_start_time', 'actual_end_time']
            data = {k: v for k, v in data.items() if k in allowed_fields}
            
        updated = job_service.update_job(job_id, data)
        if not updated:
            return {"message": "Failed to update job"}, 400
        return {"message": "Job updated successfully"}, 200
    
    @admin_required
    def delete(self, job_id):
        """Delete a job (admin only)"""
        deleted = job_service.delete_job(job_id)
        if not deleted:
            return {"message": "Job not found"}, 404
        return {"message": "Job deleted successfully"}, 200

class JobListResource(Resource):
    @token_required
    def get(self):
        """Get all jobs with optional filtering"""
        # Get query parameters for filtering
        status = request.args.get('status')
        technician_id = request.args.get('technician_id')
        customer_id = request.args.get('customer_id')
        date = request.args.get('date')
        
        # Filter based on user role
        if request.user_role == 'customer':
            # Customers can only see their own jobs
            customer_id = request.user_id
        elif request.user_role == 'technician':
            # Technicians can see their assigned jobs or all if admin
            if not technician_id:
                technician_id = request.user_id
        
        jobs = job_service.get_all_jobs(
            status=status,
            technician_id=technician_id,
            customer_id=customer_id,
            date=date
        )
        return jobs, 200
    
    @admin_required
    def post(self):
        """Create a new job"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_id', 'service_type', 'location', 'scheduled_date']
        for field in required_fields:
            if field not in data:
                return {"message": f"Missing required field: {field}"}, 400
        
        # Create job
        job_id = job_service.create_job(data)
        
        # Trigger route optimization if auto-assign is requested
        if data.get('auto_assign', False):
            routing_service.optimize_routes_for_date(data['scheduled_date'])
        
        return {"message": "Job created successfully", "job_id": job_id}, 201

class JobAssignmentResource(Resource):
    @jwt_required()
    def post(self, job_id):
        """Assign a job to a technician"""
        data = request.get_json()
        
        # Validate required fields
        if 'technician_id' not in data:
            return {"message": "Missing required field: technician_id"}, 400
        
        # Assign job
        success = job_service.assign_job(job_id, data['technician_id'])
        if not success:
            return {"message": "Failed to assign job"}, 400
        
        return {"message": "Job assigned successfully"}, 200
