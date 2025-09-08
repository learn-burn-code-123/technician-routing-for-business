from bson import ObjectId
from datetime import datetime
from models.customer import Customer
from services.db_service import DatabaseService

class CustomerService:
    """Service for customer operations"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.collection = self.db_service.get_collection('customers')
    
    def create_customer(self, customer_data):
        """Create a new customer"""
        customer = Customer.from_dict(customer_data)
        result = self.collection.insert_one(customer.__dict__)
        return str(result.inserted_id)
    
    def get_customer_by_id(self, customer_id):
        """Get a customer by ID"""
        try:
            customer_data = self.collection.find_one({"_id": ObjectId(customer_id)})
            if customer_data:
                customer = Customer.from_dict(customer_data)
                return customer.to_dict()
            return None
        except Exception as e:
            print(f"Error getting customer: {e}")
            return None
    
    def get_customer_by_email(self, email):
        """Get a customer by email"""
        try:
            customer_data = self.collection.find_one({"email": email})
            if customer_data:
                customer = Customer.from_dict(customer_data)
                return customer.to_dict()
            return None
        except Exception as e:
            print(f"Error getting customer by email: {e}")
            return None
    
    def get_customer_by_phone(self, phone):
        """Get a customer by phone"""
        try:
            customer_data = self.collection.find_one({"phone": phone})
            if customer_data:
                customer = Customer.from_dict(customer_data)
                return customer.to_dict()
            return None
        except Exception as e:
            print(f"Error getting customer by phone: {e}")
            return None
    
    def get_all_customers(self, email=None, phone=None):
        """Get all customers with optional filtering"""
        query = {}
        if email:
            query["email"] = email
        if phone:
            query["phone"] = phone
        
        customers = []
        try:
            cursor = self.collection.find(query)
            for customer_data in cursor:
                customer = Customer.from_dict(customer_data)
                customers.append(customer.to_dict())
            return customers
        except Exception as e:
            print(f"Error getting customers: {e}")
            return []
    
    def update_customer(self, customer_id, customer_data):
        """Update a customer"""
        try:
            # Get existing customer
            existing_data = self.collection.find_one({"_id": ObjectId(customer_id)})
            if not existing_data:
                return False
            
            # Update fields
            update_data = {k: v for k, v in customer_data.items() if k != '_id'}
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(customer_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating customer: {e}")
            return False
    
    def delete_customer(self, customer_id):
        """Delete a customer"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(customer_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False
