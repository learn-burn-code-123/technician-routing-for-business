from bson import ObjectId
from datetime import datetime
from models.user import User
from services.db_service import DatabaseService
from utils.password_utils import hash_password

class UserService:
    """Service for user operations"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.collection = self.db_service.get_collection('users')
    
    def create_user(self, user_data):
        """Create a new user"""
        # Hash the password
        user_data['password_hash'] = hash_password(user_data.pop('password'))
        
        user = User.from_dict(user_data)
        result = self.collection.insert_one(user.__dict__)
        return str(result.inserted_id)
    
    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        try:
            user_data = self.collection.find_one({"_id": ObjectId(user_id)})
            if user_data:
                user = User.from_dict(user_data)
                return user.to_dict()
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get a user by email"""
        try:
            user_data = self.collection.find_one({"email": email})
            if user_data:
                user = User.from_dict(user_data)
                return user.to_dict_with_password()
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def update_user(self, user_id, user_data):
        """Update a user"""
        try:
            # Get existing user
            existing_data = self.collection.find_one({"_id": ObjectId(user_id)})
            if not existing_data:
                return False
            
            # Update fields
            update_data = {k: v for k, v in user_data.items() if k != '_id' and k != 'password_hash'}
            
            # If password is being updated
            if 'password' in user_data:
                update_data['password_hash'] = hash_password(user_data['password'])
            
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, user_id):
        """Delete a user"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
