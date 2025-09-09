import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Filipino mockup data
TECHNICIANS = [
    {
        "id": 1,
        "name": "Juan Carlos Santos",
        "phone": "+63 917 123 4567",
        "email": "juan.santos@isptech.ph",
        "address": "123 Rizal Street, Makati City, Metro Manila",
        "skills": ["Fiber Installation", "Router Setup", "Network Troubleshooting"],
        "status": "available",
        "current_location": {"lat": 14.5547, "lng": 121.0244},
        "rating": 4.8
    },
    {
        "id": 2,
        "name": "Maria Elena Reyes",
        "phone": "+63 918 234 5678",
        "email": "maria.reyes@isptech.ph",
        "address": "456 Bonifacio Avenue, Quezon City, Metro Manila",
        "skills": ["Cable Installation", "Modem Setup", "Signal Testing"],
        "status": "busy",
        "current_location": {"lat": 14.6760, "lng": 121.0437},
        "rating": 4.9
    },
    {
        "id": 3,
        "name": "Roberto Miguel Cruz",
        "phone": "+63 919 345 6789",
        "email": "roberto.cruz@isptech.ph",
        "address": "789 Magsaysay Boulevard, Mandaluyong City, Metro Manila",
        "skills": ["Fiber Installation", "Network Troubleshooting", "Equipment Repair"],
        "status": "available",
        "current_location": {"lat": 14.5794, "lng": 121.0359},
        "rating": 4.7
    },
    {
        "id": 4,
        "name": "Ana Cristina Villanueva",
        "phone": "+63 920 456 7890",
        "email": "ana.villanueva@isptech.ph",
        "address": "321 Taft Avenue, Pasay City, Metro Manila",
        "skills": ["Router Setup", "WiFi Configuration", "Customer Support"],
        "status": "available",
        "current_location": {"lat": 14.5378, "lng": 120.9896},
        "rating": 4.6
    }
]

CUSTOMERS = [
    {
        "id": 1,
        "name": "Jose Antonio Mendoza",
        "phone": "+63 917 987 6543",
        "email": "jose.mendoza@gmail.com",
        "address": "Unit 12B, Sunrise Towers, Ortigas Center, Pasig City",
        "service_type": "Residential",
        "plan": "Fiber 100 Mbps"
    },
    {
        "id": 2,
        "name": "Carmen Isabella Torres",
        "phone": "+63 918 876 5432",
        "email": "carmen.torres@yahoo.com",
        "address": "567 Katipunan Avenue, Loyola Heights, Quezon City",
        "service_type": "Residential",
        "plan": "Fiber 50 Mbps"
    },
    {
        "id": 3,
        "name": "Miguel Rafael Gonzales",
        "phone": "+63 919 765 4321",
        "email": "miguel.gonzales@outlook.com",
        "address": "890 Shaw Boulevard, Kapitolyo, Pasig City",
        "service_type": "Business",
        "plan": "Fiber 200 Mbps"
    },
    {
        "id": 4,
        "name": "Sofia Gabriela Ramos",
        "phone": "+63 920 654 3210",
        "email": "sofia.ramos@gmail.com",
        "address": "234 Jupiter Street, Bel-Air, Makati City",
        "service_type": "Residential",
        "plan": "Fiber 75 Mbps"
    }
]

JOBS = [
    {
        "id": 1,
        "customer_id": 1,
        "technician_id": 1,
        "type": "Installation",
        "description": "New fiber internet installation",
        "status": "assigned",
        "priority": "high",
        "scheduled_time": "2025-01-09 14:00:00",
        "estimated_duration": 120,
        "created_at": "2025-01-09 10:00:00"
    },
    {
        "id": 2,
        "customer_id": 2,
        "technician_id": 2,
        "type": "Repair",
        "description": "Internet connection issues",
        "status": "in_progress",
        "priority": "medium",
        "scheduled_time": "2025-01-09 11:00:00",
        "estimated_duration": 90,
        "created_at": "2025-01-09 09:30:00"
    },
    {
        "id": 3,
        "customer_id": 3,
        "technician_id": None,
        "type": "Upgrade",
        "description": "Upgrade to higher speed plan",
        "status": "pending",
        "priority": "low",
        "scheduled_time": "2025-01-09 16:00:00",
        "estimated_duration": 60,
        "created_at": "2025-01-09 08:45:00"
    },
    {
        "id": 4,
        "customer_id": 4,
        "technician_id": 3,
        "type": "Maintenance",
        "description": "Routine equipment check",
        "status": "completed",
        "priority": "low",
        "scheduled_time": "2025-01-08 15:00:00",
        "estimated_duration": 45,
        "created_at": "2025-01-08 12:00:00"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/technicians')
def get_technicians():
    return jsonify(TECHNICIANS)

@app.route('/api/customers')
def get_customers():
    return jsonify(CUSTOMERS)

@app.route('/api/jobs')
def get_jobs():
    return jsonify(JOBS)

@app.route('/api/dashboard')
def get_dashboard():
    total_technicians = len(TECHNICIANS)
    available_technicians = len([t for t in TECHNICIANS if t['status'] == 'available'])
    total_jobs = len(JOBS)
    pending_jobs = len([j for j in JOBS if j['status'] == 'pending'])
    in_progress_jobs = len([j for j in JOBS if j['status'] == 'in_progress'])
    completed_jobs = len([j for j in JOBS if j['status'] == 'completed'])
    
    return jsonify({
        'technicians': {
            'total': total_technicians,
            'available': available_technicians,
            'busy': total_technicians - available_technicians
        },
        'jobs': {
            'total': total_jobs,
            'pending': pending_jobs,
            'in_progress': in_progress_jobs,
            'completed': completed_jobs
        },
        'performance': {
            'avg_response_time': '12 minutes',
            'completion_rate': '94%',
            'customer_satisfaction': '4.7/5'
        }
    })

@app.route('/api/assign_job', methods=['POST'])
def assign_job():
    data = request.json
    job_id = data.get('job_id')
    technician_id = data.get('technician_id')
    
    # Find job and technician
    job = next((j for j in JOBS if j['id'] == job_id), None)
    technician = next((t for t in TECHNICIANS if t['id'] == technician_id), None)
    
    if job and technician and technician['status'] == 'available':
        job['technician_id'] = technician_id
        job['status'] = 'assigned'
        technician['status'] = 'busy'
        
        return jsonify({'success': True, 'message': 'Job assigned successfully'})
    
    return jsonify({'success': False, 'message': 'Unable to assign job'}), 400

@app.route('/api/update_job_status', methods=['POST'])
def update_job_status():
    data = request.json
    job_id = data.get('job_id')
    new_status = data.get('status')
    
    job = next((j for j in JOBS if j['id'] == job_id), None)
    
    if job:
        job['status'] = new_status
        
        # If job is completed, make technician available
        if new_status == 'completed' and job['technician_id']:
            technician = next((t for t in TECHNICIANS if t['id'] == job['technician_id']), None)
            if technician:
                technician['status'] = 'available'
        
        return jsonify({'success': True, 'message': 'Job status updated'})
    
    return jsonify({'success': False, 'message': 'Job not found'}), 404

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
