from flask import Blueprint, jsonify
from flask_restful import Api

# Import resources
from api.resources.technician import (
    TechnicianResource, 
    TechnicianListResource,
    TechnicianProfileResource,
    TechnicianLocationResource,
    TechnicianStatusResource
)
from api.resources.job import JobResource, JobListResource, JobAssignmentResource
from api.resources.customer import CustomerResource, CustomerListResource, CustomerProfileResource
from api.resources.auth import LoginResource, RegisterResource, RefreshTokenResource
from api.resources.routing import OptimizeRoutesResource

def register_routes(app):
    # Create API
    api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(api_bp)
    
    # Auth routes
    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(RegisterResource, '/auth/register')
    api.add_resource(RefreshTokenResource, '/auth/refresh')
    
    # Technician routes
    api.add_resource(TechnicianListResource, '/technicians')
    api.add_resource(TechnicianResource, '/technicians/<string:technician_id>')
    api.add_resource(TechnicianProfileResource, '/technicians/profile')
    api.add_resource(TechnicianLocationResource, '/technicians/location')
    api.add_resource(TechnicianStatusResource, '/technicians/status')
    
    # Job routes
    api.add_resource(JobListResource, '/jobs')
    api.add_resource(JobResource, '/jobs/<string:job_id>')
    api.add_resource(JobAssignmentResource, '/jobs/<string:job_id>/assign')
    
    # Customer routes
    api.add_resource(CustomerListResource, '/customers')
    api.add_resource(CustomerResource, '/customers/<string:customer_id>')
    api.add_resource(CustomerProfileResource, '/customers/profile')
    
    # Routing routes
    api.add_resource(OptimizeRoutesResource, '/routing/optimize')
    
    # Register blueprint
    app.register_blueprint(api_bp)
    
    return app
