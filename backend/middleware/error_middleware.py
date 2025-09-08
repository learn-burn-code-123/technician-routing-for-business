from flask import jsonify
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Error handling middleware for Flask application"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the error handler with a Flask app"""
        
        # Handle 400 Bad Request errors
        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({
                'error': 'Bad Request',
                'message': str(error)
            }), 400
        
        # Handle 401 Unauthorized errors
        @app.errorhandler(401)
        def unauthorized(error):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }), 401
        
        # Handle 403 Forbidden errors
        @app.errorhandler(403)
        def forbidden(error):
            return jsonify({
                'error': 'Forbidden',
                'message': 'You do not have permission to access this resource'
            }), 403
        
        # Handle 404 Not Found errors
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'error': 'Not Found',
                'message': 'The requested resource was not found'
            }), 404
        
        # Handle 405 Method Not Allowed errors
        @app.errorhandler(405)
        def method_not_allowed(error):
            return jsonify({
                'error': 'Method Not Allowed',
                'message': 'The method is not allowed for the requested URL'
            }), 405
        
        # Handle 500 Internal Server Error
        @app.errorhandler(500)
        def internal_server_error(error):
            # Log the error
            logger.error(f"Internal Server Error: {str(error)}")
            logger.error(traceback.format_exc())
            
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }), 500
        
        # Handle generic exceptions
        @app.errorhandler(Exception)
        def handle_exception(error):
            # Log the error
            logger.error(f"Unhandled Exception: {str(error)}")
            logger.error(traceback.format_exc())
            
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }), 500
