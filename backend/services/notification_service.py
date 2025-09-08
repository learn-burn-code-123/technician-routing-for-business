import os
import requests
from datetime import datetime, timedelta
from services.customer_service import CustomerService
from services.technician_service import TechnicianService
from services.job_service import JobService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NotificationService:
    """Service for sending notifications to technicians and customers"""
    
    def __init__(self):
        self.customer_service = CustomerService()
        self.technician_service = TechnicianService()
        self.job_service = JobService()
        self.sms_api_key = os.environ.get('SMS_API_KEY')
        self.email_api_key = os.environ.get('EMAIL_API_KEY')
    
    def notify_technician_job_assignment(self, technician_id, job_id):
        """Notify a technician about a new job assignment"""
        try:
            # Get technician and job details
            technician = self.technician_service.get_technician_by_id(technician_id)
            job = self.job_service.get_job_by_id(job_id)
            
            if not technician or not job:
                return False
            
            # Get customer details
            customer = self.customer_service.get_customer_by_id(job['customer_id'])
            
            if not customer:
                return False
            
            # Prepare notification message
            message = f"New job assigned: {job['service_type']} at {customer['address']} on {job['scheduled_date']} between {job['scheduled_time_window']['start']} and {job['scheduled_time_window']['end']}."
            
            # Send notification (email and/or SMS)
            self._send_email(technician['email'], "New Job Assignment", message)
            self._send_sms(technician['phone'], message)
            
            return True
        except Exception as e:
            print(f"Error notifying technician: {e}")
            return False
    
    def notify_customer_job_scheduled(self, customer_id, job_id):
        """Notify a customer about a scheduled job"""
        try:
            # Get customer and job details
            customer = self.customer_service.get_customer_by_id(customer_id)
            job = self.job_service.get_job_by_id(job_id)
            
            if not customer or not job:
                return False
            
            # Check if technician is assigned
            technician_info = ""
            if job.get('technician_id'):
                technician = self.technician_service.get_technician_by_id(job['technician_id'])
                if technician:
                    technician_info = f" Technician {technician['name']} will be handling your service."
            
            # Prepare notification message
            message = f"Your {job['service_type']} service has been scheduled for {job['scheduled_date']} between {job['scheduled_time_window']['start']} and {job['scheduled_time_window']['end']}.{technician_info}"
            
            # Send notification (email and/or SMS)
            self._send_email(customer['email'], "Service Appointment Scheduled", message)
            self._send_sms(customer['phone'], message)
            
            return True
        except Exception as e:
            print(f"Error notifying customer: {e}")
            return False
    
    def notify_customer_technician_en_route(self, job_id):
        """Notify a customer that the technician is en route"""
        try:
            # Get job details
            job = self.job_service.get_job_by_id(job_id)
            
            if not job or not job.get('technician_id') or not job.get('customer_id'):
                return False
            
            # Get customer and technician details
            customer = self.customer_service.get_customer_by_id(job['customer_id'])
            technician = self.technician_service.get_technician_by_id(job['technician_id'])
            
            if not customer or not technician:
                return False
            
            # Prepare notification message
            eta = job.get('estimated_arrival_time', 'soon')
            message = f"Your technician {technician['name']} is on the way to your location for your {job['service_type']} service. Estimated arrival: {eta}."
            
            # Send notification (email and/or SMS)
            self._send_email(customer['email'], "Technician En Route", message)
            self._send_sms(customer['phone'], message)
            
            return True
        except Exception as e:
            print(f"Error notifying customer about technician en route: {e}")
            return False
    
    def notify_customer_job_completed(self, job_id):
        """Notify a customer that the job has been completed"""
        try:
            # Get job details
            job = self.job_service.get_job_by_id(job_id)
            
            if not job or not job.get('customer_id'):
                return False
            
            # Get customer details
            customer = self.customer_service.get_customer_by_id(job['customer_id'])
            
            if not customer:
                return False
            
            # Prepare notification message
            message = f"Your {job['service_type']} service has been completed. Thank you for choosing our service!"
            
            # Send notification (email and/or SMS)
            self._send_email(customer['email'], "Service Completed", message)
            self._send_sms(customer['phone'], message)
            
            return True
        except Exception as e:
            print(f"Error notifying customer about job completion: {e}")
            return False
    
    def send_daily_schedule_to_technician(self, technician_id, date):
        """Send the daily schedule to a technician"""
        try:
            # Get technician details
            technician = self.technician_service.get_technician_by_id(technician_id)
            
            if not technician:
                return False
            
            # Get jobs assigned to the technician for the date
            jobs = self.job_service.get_all_jobs(technician_id=technician_id, date=date)
            
            if not jobs:
                message = f"You have no jobs scheduled for {date}."
            else:
                # Build schedule message
                job_list = []
                for i, job in enumerate(jobs, 1):
                    customer = self.customer_service.get_customer_by_id(job['customer_id'])
                    customer_name = customer['name'] if customer else "Unknown Customer"
                    job_list.append(f"{i}. {job['service_type']} at {customer_name}'s location ({job['location']['address']}) - {job.get('estimated_arrival_time', 'TBD')}")
                
                message = f"Your schedule for {date}:\n\n" + "\n".join(job_list)
            
            # Send notification (email and/or SMS)
            self._send_email(technician['email'], f"Schedule for {date}", message)
            self._send_sms(technician['phone'], f"Schedule for {date} has been sent to your email.")
            
            return True
        except Exception as e:
            print(f"Error sending daily schedule: {e}")
            return False
    
    def _send_email(self, recipient, subject, message):
        """Send an email notification"""
        try:
            # If email API key is available, use email service
            if self.email_api_key:
                # This is a placeholder for an actual email service API call
                # In a real implementation, you would use a service like SendGrid, Mailgun, etc.
                print(f"Sending email to {recipient}: {subject}")
                print(f"Message: {message}")
                # Example API call (commented out)
                # response = requests.post(
                #     "https://api.emailservice.com/v1/send",
                #     headers={"Authorization": f"Bearer {self.email_api_key}"},
                #     json={
                #         "to": recipient,
                #         "subject": subject,
                #         "text": message
                #     }
                # )
                # return response.status_code == 200
                return True
            else:
                # Log the email for development purposes
                print(f"[EMAIL] To: {recipient}, Subject: {subject}, Message: {message}")
                return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _send_sms(self, phone_number, message):
        """Send an SMS notification"""
        try:
            # If SMS API key is available, use SMS service
            if self.sms_api_key:
                # This is a placeholder for an actual SMS service API call
                # In a real implementation, you would use a service like Twilio, Nexmo, etc.
                print(f"Sending SMS to {phone_number}")
                print(f"Message: {message}")
                # Example API call (commented out)
                # response = requests.post(
                #     "https://api.smsservice.com/v1/send",
                #     headers={"Authorization": f"Bearer {self.sms_api_key}"},
                #     json={
                #         "to": phone_number,
                #         "message": message
                #     }
                # )
                # return response.status_code == 200
                return True
            else:
                # Log the SMS for development purposes
                print(f"[SMS] To: {phone_number}, Message: {message}")
                return True
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
