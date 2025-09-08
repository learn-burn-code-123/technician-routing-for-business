from datetime import datetime
from bson import ObjectId

class Customer:
    """Customer model for MongoDB"""
    
    def __init__(self, name, email, phone, address, location=None, 
                 service_tier=None, notes=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address  # Full address
        self.location = location  # Coordinates for mapping
        self.service_tier = service_tier or "standard"  # standard, premium, business
        self.notes = notes or ""
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def from_dict(cls, data):
        """Create a Customer instance from a dictionary"""
        return cls(
            _id=data.get('_id'),
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            location=data.get('location'),
            service_tier=data.get('service_tier', 'standard'),
            notes=data.get('notes', "")
        )
    
    def to_dict(self):
        """Convert Customer instance to a dictionary"""
        return {
            "_id": str(self._id),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "location": self.location,
            "service_tier": self.service_tier,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
