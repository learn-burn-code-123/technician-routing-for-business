from bson import ObjectId
from datetime import datetime
from models.job import Job
from services.db_service import DatabaseService

class JobService:
    """Service for job operations"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.collection = self.db_service.get_collection('jobs')
    
    def create_job(self, job_data):
        """Create a new job"""
        job = Job.from_dict(job_data)
        result = self.collection.insert_one(job.__dict__)
        return str(result.inserted_id)
    
    def get_job_by_id(self, job_id):
        """Get a job by ID"""
        try:
            job_data = self.collection.find_one({"_id": ObjectId(job_id)})
            if job_data:
                job = Job.from_dict(job_data)
                return job.to_dict()
            return None
        except Exception as e:
            print(f"Error getting job: {e}")
            return None
    
    def get_all_jobs(self, status=None, technician_id=None, customer_id=None, date=None):
        """Get all jobs with optional filtering"""
        query = {}
        if status:
            query["status"] = status
        if technician_id:
            query["technician_id"] = technician_id
        if customer_id:
            query["customer_id"] = customer_id
        if date:
            query["scheduled_date"] = date
        
        jobs = []
        try:
            cursor = self.collection.find(query)
            for job_data in cursor:
                job = Job.from_dict(job_data)
                jobs.append(job.to_dict())
            return jobs
        except Exception as e:
            print(f"Error getting jobs: {e}")
            return []
    
    def update_job(self, job_id, job_data):
        """Update a job"""
        try:
            # Get existing job
            existing_data = self.collection.find_one({"_id": ObjectId(job_id)})
            if not existing_data:
                return False
            
            # Update fields
            update_data = {k: v for k, v in job_data.items() if k != '_id'}
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating job: {e}")
            return False
    
    def delete_job(self, job_id):
        """Delete a job"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(job_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting job: {e}")
            return False
    
    def assign_job(self, job_id, technician_id):
        """Assign a job to a technician"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(job_id)},
                {
                    "$set": {
                        "technician_id": technician_id,
                        "status": "assigned",
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error assigning job: {e}")
            return False
    
    def update_job_status(self, job_id, status, actual_start_time=None, actual_end_time=None):
        """Update a job's status"""
        try:
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow()
            }
            
            if actual_start_time:
                update_data["actual_start_time"] = actual_start_time
            
            if actual_end_time:
                update_data["actual_end_time"] = actual_end_time
            
            result = self.collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating job status: {e}")
            return False
    
    def get_jobs_for_date_range(self, start_date, end_date, technician_id=None):
        """Get jobs for a date range with optional technician filtering"""
        query = {
            "scheduled_date": {"$gte": start_date, "$lte": end_date}
        }
        
        if technician_id:
            query["technician_id"] = technician_id
        
        jobs = []
        try:
            cursor = self.collection.find(query)
            for job_data in cursor:
                job = Job.from_dict(job_data)
                jobs.append(job.to_dict())
            return jobs
        except Exception as e:
            print(f"Error getting jobs for date range: {e}")
            return []
