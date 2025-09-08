from datetime import datetime
from bson import ObjectId

class Technician:
    """Technician model for MongoDB"""
    
    def __init__(self, name, email, phone, skills, location=None, status="available", 
                 current_location=None, working_hours=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.name = name
        self.email = email
        self.phone = phone
        self.skills = skills  # List of skills/certifications
        self.location = location  # Home/base location
        self.status = status  # available, busy, off-duty
        self.current_location = current_location  # Current GPS coordinates
        self.working_hours = working_hours or {
            "monday": {"start": "09:00", "end": "17:00"},
            "tuesday": {"start": "09:00", "end": "17:00"},
            "wednesday": {"start": "09:00", "end": "17:00"},
            "thursday": {"start": "09:00", "end": "17:00"},
            "friday": {"start": "09:00", "end": "17:00"},
            "saturday": None,
            "sunday": None
        }
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def from_dict(cls, data):
        """Create a Technician instance from a dictionary"""
        return cls(
            _id=data.get('_id'),
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            skills=data.get('skills', []),
            location=data.get('location'),
            status=data.get('status', 'available'),
            current_location=data.get('current_location'),
            working_hours=data.get('working_hours')
        )
    
    def to_dict(self):
        """Convert Technician instance to a dictionary"""
        return {
            "_id": str(self._id),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills,
            "location": self.location,
            "status": self.status,
            "current_location": self.current_location,
            "working_hours": self.working_hours,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
