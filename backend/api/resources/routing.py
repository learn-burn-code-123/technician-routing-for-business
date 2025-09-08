from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.routing_service import RoutingService

routing_service = RoutingService()

class OptimizeRoutesResource(Resource):
    @jwt_required()
    def post(self):
        """Optimize routes for technicians"""
        data = request.get_json()
        
        # Validate required fields
        if 'date' not in data:
            return {"message": "Missing required field: date"}, 400
        
        # Optional parameters
        technician_ids = data.get('technician_ids', None)  # If None, optimize for all technicians
        consider_traffic = data.get('consider_traffic', True)
        consider_weather = data.get('consider_weather', True)
        
        # Run optimization
        try:
            result = routing_service.optimize_routes_for_date(
                date=data['date'],
                technician_ids=technician_ids,
                consider_traffic=consider_traffic,
                consider_weather=consider_weather
            )
            
            return {
                "message": "Routes optimized successfully",
                "optimized_routes": result['routes'],
                "metrics": result['metrics']
            }, 200
            
        except Exception as e:
            return {"message": f"Failed to optimize routes: {str(e)}"}, 500
