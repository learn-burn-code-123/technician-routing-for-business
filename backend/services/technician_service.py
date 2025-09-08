from bson import ObjectId
from models.technician import Technician
from services.db_service import DatabaseService

class TechnicianService:
    """Service for technician operations"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.collection = self.db_service.get_collection('technicians')
    
    def create_technician(self, technician_data):
        """Create a new technician"""
        technician = Technician.from_dict(technician_data)
        result = self.collection.insert_one(technician.__dict__)
        return str(result.inserted_id)
    
    def get_technician_by_id(self, technician_id):
        """Get a technician by ID"""
        try:
            technician_data = self.collection.find_one({"_id": ObjectId(technician_id)})
            if technician_data:
                technician = Technician.from_dict(technician_data)
                return technician.to_dict()
            return None
        except Exception as e:
            print(f"Error getting technician: {e}")
            return None
    
    def get_all_technicians(self, status=None, skill=None):
        """Get all technicians with optional filtering"""
        query = {}
        if status:
            query["status"] = status
        if skill:
            query["skills"] = {"$in": [skill]}
        
        technicians = []
        try:
            cursor = self.collection.find(query)
            for technician_data in cursor:
                technician = Technician.from_dict(technician_data)
                technicians.append(technician.to_dict())
            return technicians
        except Exception as e:
            print(f"Error getting technicians: {e}")
            return []
    
    def update_technician(self, technician_id, technician_data):
        """Update a technician"""
        try:
            # Get existing technician
            existing_data = self.collection.find_one({"_id": ObjectId(technician_id)})
            if not existing_data:
                return False
            
            # Update fields
            update_data = {k: v for k, v in technician_data.items() if k != '_id'}
            result = self.collection.update_one(
                {"_id": ObjectId(technician_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating technician: {e}")
            return False
    
    def delete_technician(self, technician_id):
        """Delete a technician"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(technician_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting technician: {e}")
            return False
    
    def update_technician_location(self, technician_id, location):
        """Update a technician's current location"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(technician_id)},
                {"$set": {"current_location": location}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating technician location: {e}")
            return False
    
    def update_technician_status(self, technician_id, status):
        """Update a technician's status"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(technician_id)},
                {"$set": {"status": status}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating technician status: {e}")
            return False
