from flask_cors import CORS

def setup_cors(app):
    """Configure CORS for the Flask application"""
    
    # Set up CORS with secure defaults
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",  # Frontend development server
                "http://localhost:5000",  # Backend development server
                "https://isp-technician-routing.example.com"  # Production domain (replace with actual domain)
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": [
                "Content-Type", 
                "Authorization", 
                "X-Requested-With"
            ],
            "expose_headers": [
                "Content-Length", 
                "X-Total-Count"
            ],
            "supports_credentials": True,
            "max_age": 86400  # Cache preflight requests for 24 hours
        }
    })
    
    return app
