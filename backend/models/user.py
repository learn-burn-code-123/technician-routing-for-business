from datetime import datetime
from bson import ObjectId

class User:
    """User model for MongoDB"""
    
    def __init__(self, name, email, password_hash, role, technician_id=None, 
                 customer_id=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role  # admin, technician, customer
        self.technician_id = technician_id  # Only for technician role
        self.customer_id = customer_id  # Only for customer role
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def from_dict(cls, data):
        """Create a User instance from a dictionary"""
        return cls(
            _id=data.get('_id'),
            name=data.get('name'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            role=data.get('role'),
            technician_id=data.get('technician_id'),
            customer_id=data.get('customer_id')
        )
    
    def to_dict(self):
        """Convert User instance to a dictionary"""
        return {
            "_id": str(self._id),
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "technician_id": self.technician_id,
            "customer_id": self.customer_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def to_dict_with_password(self):
        """Convert User instance to a dictionary including password hash"""
        user_dict = self.to_dict()
        user_dict['password_hash'] = self.password_hash
        return user_dict
