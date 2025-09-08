from datetime import datetime
from bson import ObjectId

class Job:
    """Job model for MongoDB"""
    
    def __init__(self, customer_id, service_type, location, scheduled_date, 
                 scheduled_time_window=None, status="pending", priority="normal",
                 estimated_duration=60, technician_id=None, notes=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.customer_id = customer_id
        self.service_type = service_type  # installation, repair, maintenance
        self.location = location  # Address and coordinates
        self.scheduled_date = scheduled_date  # YYYY-MM-DD
        self.scheduled_time_window = scheduled_time_window or {"start": "09:00", "end": "17:00"}
        self.status = status  # pending, assigned, in_progress, completed, cancelled
        self.priority = priority  # low, normal, high, urgent
        self.estimated_duration = estimated_duration  # in minutes
        self.technician_id = technician_id  # Assigned technician ID
        self.notes = notes or ""
        self.actual_start_time = None
        self.actual_end_time = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def from_dict(cls, data):
        """Create a Job instance from a dictionary"""
        return cls(
            _id=data.get('_id'),
            customer_id=data.get('customer_id'),
            service_type=data.get('service_type'),
            location=data.get('location'),
            scheduled_date=data.get('scheduled_date'),
            scheduled_time_window=data.get('scheduled_time_window'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'normal'),
            estimated_duration=data.get('estimated_duration', 60),
            technician_id=data.get('technician_id'),
            notes=data.get('notes', "")
        )
    
    def to_dict(self):
        """Convert Job instance to a dictionary"""
        return {
            "_id": str(self._id),
            "customer_id": self.customer_id,
            "service_type": self.service_type,
            "location": self.location,
            "scheduled_date": self.scheduled_date,
            "scheduled_time_window": self.scheduled_time_window,
            "status": self.status,
            "priority": self.priority,
            "estimated_duration": self.estimated_duration,
            "technician_id": self.technician_id,
            "notes": self.notes,
            "actual_start_time": self.actual_start_time.isoformat() if self.actual_start_time else None,
            "actual_end_time": self.actual_end_time.isoformat() if self.actual_end_time else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
