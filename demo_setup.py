#!/usr/bin/env python3
"""
Demo Setup Script for ISP Technician Routing System
Creates sample data and demonstrates the system functionality
"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta
import time

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# API Base URL
API_BASE = "http://localhost:5000/api/v1"

class DemoSetup:
    def __init__(self):
        self.tokens = {}
        self.users = {}
        self.sample_data = {
            'customers': [],
            'technicians': [],
            'jobs': []
        }
    
    def create_sample_users(self):
        """Create sample users for demo"""
        print("🔧 Creating sample users...")
        
        # Sample users to create
        users = [
            {
                "name": "Admin User",
                "email": "admin@isp.com",
                "password": "admin123",
                "role": "admin"
            },
            {
                "name": "John Smith",
                "email": "john.technician@isp.com", 
                "password": "tech123",
                "role": "technician"
            },
            {
                "name": "Sarah Johnson",
                "email": "sarah.technician@isp.com",
                "password": "tech123", 
                "role": "technician"
            },
            {
                "name": "Mike Wilson",
                "email": "mike.customer@email.com",
                "password": "customer123",
                "role": "customer"
            },
            {
                "name": "Lisa Brown",
                "email": "lisa.customer@email.com",
                "password": "customer123",
                "role": "customer"
            }
        ]
        
        for user in users:
            try:
                response = requests.post(f"{API_BASE}/auth/register", json=user)
                if response.status_code == 201:
                    print(f"✅ Created user: {user['name']} ({user['role']})")
                else:
                    print(f"⚠️  User {user['name']} may already exist")
            except Exception as e:
                print(f"❌ Error creating user {user['name']}: {e}")
    
    def login_users(self):
        """Login all demo users and store tokens"""
        print("\n🔑 Logging in demo users...")
        
        login_credentials = [
            {"email": "admin@isp.com", "password": "admin123", "role": "admin"},
            {"email": "john.technician@isp.com", "password": "tech123", "role": "technician"},
            {"email": "sarah.technician@isp.com", "password": "tech123", "role": "technician"},
            {"email": "mike.customer@email.com", "password": "customer123", "role": "customer"},
            {"email": "lisa.customer@email.com", "password": "customer123", "role": "customer"}
        ]
        
        for creds in login_credentials:
            try:
                response = requests.post(f"{API_BASE}/auth/login", json={
                    "email": creds["email"],
                    "password": creds["password"]
                })
                
                if response.status_code == 200:
                    data = response.json()
                    self.tokens[creds["role"]] = data["access_token"]
                    self.users[creds["role"]] = data["user"]
                    print(f"✅ Logged in: {data['user']['name']}")
                else:
                    print(f"❌ Login failed for {creds['email']}")
            except Exception as e:
                print(f"❌ Error logging in {creds['email']}: {e}")
    
    def create_sample_data(self):
        """Create sample technicians, customers, and jobs"""
        print("\n📊 Creating sample data...")
        
        if "admin" not in self.tokens:
            print("❌ Admin token not available")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
        
        # Create sample technicians
        technicians = [
            {
                "name": "John Smith",
                "email": "john.technician@isp.com",
                "phone": "+1-555-0101",
                "skills": ["fiber_installation", "router_setup", "troubleshooting"],
                "location": {"address": "123 Tech St, San Francisco, CA", "lat": 37.7749, "lng": -122.4194},
                "status": "available"
            },
            {
                "name": "Sarah Johnson", 
                "email": "sarah.technician@isp.com",
                "phone": "+1-555-0102",
                "skills": ["cable_installation", "modem_setup", "network_config"],
                "location": {"address": "456 Service Ave, San Francisco, CA", "lat": 37.7849, "lng": -122.4094},
                "status": "available"
            }
        ]
        
        for tech in technicians:
            try:
                response = requests.post(f"{API_BASE}/technicians", json=tech, headers=headers)
                if response.status_code == 201:
                    print(f"✅ Created technician: {tech['name']}")
                    self.sample_data['technicians'].append(response.json())
            except Exception as e:
                print(f"❌ Error creating technician {tech['name']}: {e}")
        
        # Create sample customers
        customers = [
            {
                "name": "Mike Wilson",
                "email": "mike.customer@email.com", 
                "phone": "+1-555-0201",
                "address": "789 Customer Ln, San Francisco, CA",
                "service_tier": "premium"
            },
            {
                "name": "Lisa Brown",
                "email": "lisa.customer@email.com",
                "phone": "+1-555-0202", 
                "address": "321 Home St, San Francisco, CA",
                "service_tier": "standard"
            }
        ]
        
        for customer in customers:
            try:
                response = requests.post(f"{API_BASE}/customers", json=customer, headers=headers)
                if response.status_code == 201:
                    print(f"✅ Created customer: {customer['name']}")
                    self.sample_data['customers'].append(response.json())
            except Exception as e:
                print(f"❌ Error creating customer {customer['name']}: {e}")
        
        # Create sample jobs
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        jobs = [
            {
                "customer_id": "customer_id_1",  # Will be replaced with actual ID
                "service_type": "fiber_installation",
                "location": {
                    "address": "789 Customer Ln, San Francisco, CA",
                    "lat": 37.7649,
                    "lng": -122.4294
                },
                "scheduled_date": tomorrow,
                "scheduled_time_window": {"start": "09:00", "end": "12:00"},
                "estimated_duration": 120,
                "status": "pending"
            },
            {
                "customer_id": "customer_id_2",  # Will be replaced with actual ID
                "service_type": "router_setup", 
                "location": {
                    "address": "321 Home St, San Francisco, CA",
                    "lat": 37.7549,
                    "lng": -122.4394
                },
                "scheduled_date": tomorrow,
                "scheduled_time_window": {"start": "13:00", "end": "16:00"},
                "estimated_duration": 90,
                "status": "pending"
            }
        ]
        
        for i, job in enumerate(jobs):
            try:
                # Replace with actual customer ID if available
                if i < len(self.sample_data['customers']):
                    job["customer_id"] = self.sample_data['customers'][i].get('customer_id', f"customer_{i+1}")
                
                response = requests.post(f"{API_BASE}/jobs", json=job, headers=headers)
                if response.status_code == 201:
                    print(f"✅ Created job: {job['service_type']}")
                    self.sample_data['jobs'].append(response.json())
            except Exception as e:
                print(f"❌ Error creating job {job['service_type']}: {e}")
    
    def demo_admin_view(self):
        """Demonstrate admin functionality"""
        print("\n" + "="*50)
        print("🔧 ADMIN VIEW DEMO")
        print("="*50)
        
        if "admin" not in self.tokens:
            print("❌ Admin token not available")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
        
        # View all technicians
        print("\n📋 Viewing all technicians:")
        try:
            response = requests.get(f"{API_BASE}/technicians", headers=headers)
            if response.status_code == 200:
                technicians = response.json()
                for tech in technicians[:2]:  # Show first 2
                    print(f"  • {tech.get('name', 'N/A')} - Status: {tech.get('status', 'N/A')} - Skills: {', '.join(tech.get('skills', []))}")
            else:
                print(f"❌ Error fetching technicians: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # View all jobs
        print("\n📋 Viewing all jobs:")
        try:
            response = requests.get(f"{API_BASE}/jobs", headers=headers)
            if response.status_code == 200:
                jobs = response.json()
                for job in jobs[:3]:  # Show first 3
                    print(f"  • {job.get('service_type', 'N/A')} - Status: {job.get('status', 'N/A')} - Date: {job.get('scheduled_date', 'N/A')}")
            else:
                print(f"❌ Error fetching jobs: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Optimize routes
        print("\n🗺️  Optimizing technician routes:")
        try:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            response = requests.post(f"{API_BASE}/routing/optimize", json={
                "date": tomorrow,
                "consider_traffic": True,
                "consider_weather": False
            }, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Route optimization completed")
                print(f"  📊 Optimized routes for {len(result.get('routes', []))} technicians")
            else:
                print(f"❌ Route optimization failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def demo_technician_view(self):
        """Demonstrate technician functionality"""
        print("\n" + "="*50)
        print("👷 TECHNICIAN VIEW DEMO")
        print("="*50)
        
        if "technician" not in self.tokens:
            print("❌ Technician token not available")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['technician']}"}
        
        # View technician profile
        print("\n👤 Technician Profile:")
        try:
            response = requests.get(f"{API_BASE}/technicians/profile", headers=headers)
            if response.status_code == 200:
                profile = response.json()
                print(f"  Name: {profile.get('name', 'N/A')}")
                print(f"  Status: {profile.get('status', 'N/A')}")
                print(f"  Skills: {', '.join(profile.get('skills', []))}")
            else:
                print(f"❌ Error fetching profile: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # View assigned jobs
        print("\n📋 My Assigned Jobs:")
        try:
            response = requests.get(f"{API_BASE}/jobs", headers=headers)
            if response.status_code == 200:
                jobs = response.json()
                if jobs:
                    for job in jobs[:2]:  # Show first 2
                        print(f"  • {job.get('service_type', 'N/A')} - {job.get('scheduled_date', 'N/A')} {job.get('scheduled_time_window', {}).get('start', '')}")
                        print(f"    Location: {job.get('location', {}).get('address', 'N/A')}")
                        print(f"    Status: {job.get('status', 'N/A')}")
                else:
                    print("  No jobs assigned yet")
            else:
                print(f"❌ Error fetching jobs: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Update location
        print("\n📍 Updating location:")
        try:
            response = requests.put(f"{API_BASE}/technicians/location", json={
                "location": {"lat": 37.7849, "lng": -122.4094}
            }, headers=headers)
            
            if response.status_code == 200:
                print("  ✅ Location updated successfully")
            else:
                print(f"❌ Error updating location: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Update status
        print("\n🔄 Updating status to 'busy':")
        try:
            response = requests.put(f"{API_BASE}/technicians/status", json={
                "status": "busy"
            }, headers=headers)
            
            if response.status_code == 200:
                print("  ✅ Status updated to busy")
            else:
                print(f"❌ Error updating status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def demo_customer_view(self):
        """Demonstrate customer functionality"""
        print("\n" + "="*50)
        print("👤 CUSTOMER VIEW DEMO")
        print("="*50)
        
        if "customer" not in self.tokens:
            print("❌ Customer token not available")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['customer']}"}
        
        # View customer profile
        print("\n👤 Customer Profile:")
        try:
            response = requests.get(f"{API_BASE}/customers/profile", headers=headers)
            if response.status_code == 200:
                profile = response.json()
                print(f"  Name: {profile.get('name', 'N/A')}")
                print(f"  Email: {profile.get('email', 'N/A')}")
                print(f"  Service Tier: {profile.get('service_tier', 'N/A')}")
                print(f"  Address: {profile.get('address', 'N/A')}")
            else:
                print(f"❌ Error fetching profile: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # View my appointments
        print("\n📅 My Appointments:")
        try:
            response = requests.get(f"{API_BASE}/jobs", headers=headers)
            if response.status_code == 200:
                jobs = response.json()
                if jobs:
                    for job in jobs:
                        print(f"  • {job.get('service_type', 'N/A')} - {job.get('scheduled_date', 'N/A')}")
                        print(f"    Time: {job.get('scheduled_time_window', {}).get('start', '')} - {job.get('scheduled_time_window', {}).get('end', '')}")
                        print(f"    Status: {job.get('status', 'N/A')}")
                        if job.get('technician_name'):
                            print(f"    Technician: {job.get('technician_name')}")
                        if job.get('estimated_arrival_time'):
                            print(f"    ETA: {job.get('estimated_arrival_time')}")
                        print()
                else:
                    print("  No appointments scheduled")
            else:
                print(f"❌ Error fetching appointments: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Update profile
        print("\n✏️  Updating profile:")
        try:
            response = requests.put(f"{API_BASE}/customers/profile", json={
                "phone": "+1-555-0299"
            }, headers=headers)
            
            if response.status_code == 200:
                print("  ✅ Profile updated successfully")
            else:
                print(f"❌ Error updating profile: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run_demo(self):
        """Run the complete demo"""
        print("🚀 Starting ISP Technician Routing System Demo")
        print("="*60)
        
        # Setup phase
        self.create_sample_users()
        time.sleep(1)
        self.login_users()
        time.sleep(1)
        self.create_sample_data()
        time.sleep(1)
        
        # Demo each view
        self.demo_admin_view()
        time.sleep(2)
        self.demo_technician_view()
        time.sleep(2)
        self.demo_customer_view()
        
        print("\n" + "="*60)
        print("✅ Demo completed successfully!")
        print("\n📱 To see the full interfaces:")
        print("  • Customer Portal: http://localhost:3000")
        print("  • Mobile App: Use Expo Go with 'expo start'")
        print("  • API Documentation: See API_DOCUMENTATION.md")
        print("="*60)

if __name__ == "__main__":
    demo = DemoSetup()
    demo.run_demo()
