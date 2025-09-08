#!/usr/bin/env python3
"""
Mock Demo for ISP Technician Routing System
Demonstrates the three user interfaces without requiring backend setup
"""

import time
import json
from datetime import datetime, timedelta

class MockDemo:
    def __init__(self):
        self.sample_data = self.create_sample_data()
    
    def create_sample_data(self):
        """Create mock data for demonstration"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        return {
            "users": {
                "admin": {
                    "id": "admin_001",
                    "name": "Admin User",
                    "email": "admin@isp.com",
                    "role": "admin"
                },
                "technician": {
                    "id": "tech_001", 
                    "name": "John Smith",
                    "email": "john.technician@isp.com",
                    "role": "technician",
                    "status": "available",
                    "skills": ["fiber_installation", "router_setup", "troubleshooting"],
                    "current_location": {"lat": 37.7749, "lng": -122.4194}
                },
                "customer": {
                    "id": "cust_001",
                    "name": "Mike Wilson", 
                    "email": "mike.customer@email.com",
                    "role": "customer",
                    "service_tier": "premium",
                    "address": "789 Customer Ln, San Francisco, CA"
                }
            },
            "technicians": [
                {
                    "id": "tech_001",
                    "name": "John Smith",
                    "email": "john.technician@isp.com",
                    "phone": "+1-555-0101",
                    "status": "available",
                    "skills": ["fiber_installation", "router_setup", "troubleshooting"],
                    "current_location": {"lat": 37.7749, "lng": -122.4194},
                    "jobs_today": 3,
                    "jobs_completed": 2
                },
                {
                    "id": "tech_002", 
                    "name": "Sarah Johnson",
                    "email": "sarah.technician@isp.com",
                    "phone": "+1-555-0102",
                    "status": "busy",
                    "skills": ["cable_installation", "modem_setup", "network_config"],
                    "current_location": {"lat": 37.7849, "lng": -122.4094},
                    "jobs_today": 4,
                    "jobs_completed": 3
                }
            ],
            "customers": [
                {
                    "id": "cust_001",
                    "name": "Mike Wilson",
                    "email": "mike.customer@email.com",
                    "phone": "+1-555-0201",
                    "address": "789 Customer Ln, San Francisco, CA",
                    "service_tier": "premium"
                },
                {
                    "id": "cust_002",
                    "name": "Lisa Brown", 
                    "email": "lisa.customer@email.com",
                    "phone": "+1-555-0202",
                    "address": "321 Home St, San Francisco, CA",
                    "service_tier": "standard"
                }
            ],
            "jobs": [
                {
                    "id": "job_001",
                    "customer_id": "cust_001",
                    "customer_name": "Mike Wilson",
                    "technician_id": "tech_001",
                    "technician_name": "John Smith",
                    "service_type": "fiber_installation",
                    "status": "assigned",
                    "scheduled_date": tomorrow,
                    "scheduled_time_window": {"start": "09:00", "end": "12:00"},
                    "estimated_duration": 120,
                    "estimated_arrival_time": "09:15",
                    "location": {
                        "address": "789 Customer Ln, San Francisco, CA",
                        "lat": 37.7649,
                        "lng": -122.4294
                    }
                },
                {
                    "id": "job_002",
                    "customer_id": "cust_002", 
                    "customer_name": "Lisa Brown",
                    "technician_id": "tech_002",
                    "technician_name": "Sarah Johnson",
                    "service_type": "router_setup",
                    "status": "in_progress",
                    "scheduled_date": datetime.now().strftime("%Y-%m-%d"),
                    "scheduled_time_window": {"start": "13:00", "end": "16:00"},
                    "estimated_duration": 90,
                    "actual_start_time": "13:15",
                    "location": {
                        "address": "321 Home St, San Francisco, CA",
                        "lat": 37.7549,
                        "lng": -122.4394
                    }
                },
                {
                    "id": "job_003",
                    "customer_id": "cust_001",
                    "customer_name": "Mike Wilson", 
                    "technician_id": "tech_001",
                    "technician_name": "John Smith",
                    "service_type": "troubleshooting",
                    "status": "completed",
                    "scheduled_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                    "scheduled_time_window": {"start": "10:00", "end": "12:00"},
                    "estimated_duration": 60,
                    "actual_start_time": "10:05",
                    "actual_end_time": "11:30",
                    "location": {
                        "address": "789 Customer Ln, San Francisco, CA",
                        "lat": 37.7649,
                        "lng": -122.4294
                    }
                }
            ]
        }
    
    def print_header(self, title, icon):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"{icon} {title}")
        print("="*60)
    
    def print_section(self, title):
        """Print a section header"""
        print(f"\n📋 {title}:")
        print("-" * 40)
    
    def demo_admin_view(self):
        """Demonstrate admin dashboard functionality"""
        self.print_header("ADMIN DASHBOARD DEMO", "🔧")
        
        print("\n🎯 Admin Overview:")
        print("  • Total Technicians: 2")
        print("  • Active Jobs: 2") 
        print("  • Completed Today: 3")
        print("  • Customer Satisfaction: 94%")
        
        self.print_section("Technician Management")
        for tech in self.sample_data["technicians"]:
            status_icon = "🟢" if tech["status"] == "available" else "🔴" if tech["status"] == "busy" else "⚪"
            print(f"  {status_icon} {tech['name']}")
            print(f"     Status: {tech['status'].title()}")
            print(f"     Skills: {', '.join(tech['skills'])}")
            print(f"     Today: {tech['jobs_completed']}/{tech['jobs_today']} jobs completed")
            print(f"     Location: {tech['current_location']['lat']:.4f}, {tech['current_location']['lng']:.4f}")
            print()
        
        self.print_section("Job Queue Management")
        for job in self.sample_data["jobs"]:
            status_icons = {
                "pending": "⏳",
                "assigned": "📋", 
                "in_progress": "🔧",
                "completed": "✅",
                "cancelled": "❌"
            }
            icon = status_icons.get(job["status"], "❓")
            print(f"  {icon} Job #{job['id'][-3:]}: {job['service_type']}")
            print(f"     Customer: {job['customer_name']}")
            print(f"     Technician: {job.get('technician_name', 'Unassigned')}")
            print(f"     Date: {job['scheduled_date']} {job['scheduled_time_window']['start']}-{job['scheduled_time_window']['end']}")
            print(f"     Status: {job['status'].title()}")
            print()
        
        self.print_section("Route Optimization")
        print("  🗺️  Running optimization algorithm...")
        time.sleep(1)
        print("  ✅ Routes optimized for 2 technicians")
        print("  📊 Estimated time savings: 45 minutes")
        print("  🚗 Total distance reduced: 12.3 miles")
        print("  📍 Optimal route sequence calculated")
        
        self.print_section("Real-time Analytics")
        print("  📈 Average job completion time: 87 minutes")
        print("  🎯 On-time arrival rate: 92%")
        print("  📞 Customer satisfaction score: 4.7/5.0")
        print("  ⚡ System response time: 0.3s")
    
    def demo_technician_view(self):
        """Demonstrate technician mobile app functionality"""
        self.print_header("TECHNICIAN MOBILE APP DEMO", "👷")
        
        tech = self.sample_data["users"]["technician"]
        print(f"\n👤 Welcome back, {tech['name']}!")
        print(f"   Status: {tech['status'].title()}")
        print(f"   Today's Progress: 2/3 jobs completed")
        
        self.print_section("Today's Schedule")
        tech_jobs = [job for job in self.sample_data["jobs"] if job.get("technician_id") == tech["id"]]
        
        for job in tech_jobs:
            status_icons = {
                "assigned": "📋",
                "in_progress": "🔧", 
                "completed": "✅"
            }
            icon = status_icons.get(job["status"], "❓")
            
            print(f"  {icon} {job['service_type'].replace('_', ' ').title()}")
            print(f"     📍 {job['location']['address']}")
            print(f"     ⏰ {job['scheduled_time_window']['start']} - {job['scheduled_time_window']['end']}")
            print(f"     👤 Customer: {job['customer_name']}")
            
            if job["status"] == "assigned":
                print(f"     🚗 ETA: {job.get('estimated_arrival_time', 'Calculating...')}")
                print("     🎯 [START JOB] button available")
            elif job["status"] == "in_progress":
                print(f"     ▶️  Started: {job.get('actual_start_time', 'N/A')}")
                print("     ✅ [COMPLETE JOB] button available")
            elif job["status"] == "completed":
                print(f"     ✅ Completed: {job.get('actual_end_time', 'N/A')}")
            print()
        
        self.print_section("Interactive Map View")
        print("  🗺️  Current Location: San Francisco, CA")
        print("  📍 Next Job: 0.8 miles away (4 min drive)")
        print("  🚦 Traffic Status: Light traffic")
        print("  🧭 Navigation: Turn-by-turn directions available")
        
        self.print_section("Job Actions")
        print("  📱 Update job status: Assigned → In Progress → Completed")
        print("  📍 Share real-time location with customers")
        print("  📝 Add job notes and completion details")
        print("  📞 Contact customer directly from app")
        print("  📷 Upload photos of completed work")
        
        self.print_section("Profile & Settings")
        print(f"  👤 Name: {tech['name']}")
        print(f"  📧 Email: {tech['email']}")
        print(f"  🛠️  Skills: {', '.join(tech['skills'])}")
        print("  🔄 Status: Available/Busy/Off-duty toggle")
        print("  📍 Location sharing: Enabled")
    
    def demo_customer_view(self):
        """Demonstrate customer web portal functionality"""
        self.print_header("CUSTOMER WEB PORTAL DEMO", "👤")
        
        customer = self.sample_data["users"]["customer"]
        print(f"\n🏠 Welcome, {customer['name']}!")
        print(f"   Account: {customer['service_tier'].title()} Customer")
        print(f"   Address: {customer['address']}")
        
        self.print_section("My Appointments")
        customer_jobs = [job for job in self.sample_data["jobs"] if job.get("customer_id") == customer["id"]]
        
        for job in customer_jobs:
            status_colors = {
                "assigned": "🔵",
                "in_progress": "🟡", 
                "completed": "🟢"
            }
            color = status_colors.get(job["status"], "⚪")
            
            print(f"  {color} {job['service_type'].replace('_', ' ').title()}")
            print(f"     📅 {job['scheduled_date']}")
            print(f"     ⏰ {job['scheduled_time_window']['start']} - {job['scheduled_time_window']['end']}")
            print(f"     📍 {job['location']['address']}")
            
            if job.get("technician_name"):
                print(f"     👷 Technician: {job['technician_name']}")
                
            if job["status"] == "assigned":
                print(f"     🚗 Estimated Arrival: {job.get('estimated_arrival_time', 'TBD')}")
                print("     📱 You'll receive SMS updates")
            elif job["status"] == "in_progress":
                print(f"     ▶️  Service started at {job.get('actual_start_time', 'N/A')}")
                print("     🔴 Technician is currently on-site")
            elif job["status"] == "completed":
                print(f"     ✅ Completed at {job.get('actual_end_time', 'N/A')}")
                print("     ⭐ Rate your experience")
            print()
        
        self.print_section("Real-time Tracking")
        active_job = next((job for job in customer_jobs if job["status"] in ["assigned", "in_progress"]), None)
        if active_job:
            print(f"  🎯 Tracking: {active_job['service_type'].replace('_', ' ').title()}")
            if active_job["status"] == "assigned":
                print("  🚗 Technician is en route")
                print(f"  📍 ETA: {active_job.get('estimated_arrival_time', 'Calculating...')}")
                print("  📱 Live location updates every 2 minutes")
            else:
                print("  🔧 Technician is on-site working")
                print("  ⏱️  Estimated completion: 30 minutes")
        else:
            print("  📅 No active appointments to track")
        
        self.print_section("Technician Information")
        if active_job and active_job.get("technician_name"):
            print(f"  👷 {active_job['technician_name']}")
            print("  ⭐ Rating: 4.8/5.0 (127 reviews)")
            print("  🛠️  Specializes in: Fiber installation, Router setup")
            print("  📞 Contact: Available through app")
            print("  🚗 Vehicle: ISP Van #247")
        else:
            print("  👷 Technician will be assigned 24 hours before appointment")
        
        self.print_section("Account Management")
        print(f"  👤 Name: {customer['name']}")
        print(f"  📧 Email: {customer['email']}")
        print(f"  📍 Service Address: {customer['address']}")
        print(f"  💎 Service Tier: {customer['service_tier'].title()}")
        print("  📝 Update profile information")
        print("  📞 Contact customer support")
        print("  📋 View service history")
    
    def demo_system_features(self):
        """Demonstrate key system features"""
        self.print_header("SYSTEM FEATURES OVERVIEW", "⚡")
        
        self.print_section("Smart Routing Algorithm")
        print("  🧠 AI-powered job assignment")
        print("  🗺️  Real-time traffic consideration")
        print("  🌤️  Weather impact analysis")
        print("  📊 Workload balancing")
        print("  ⚡ Sub-second optimization")
        
        self.print_section("Real-time Communication")
        print("  📱 SMS notifications to customers")
        print("  📧 Email updates and confirmations")
        print("  🔔 Push notifications to mobile app")
        print("  📍 Live location sharing")
        print("  💬 In-app messaging")
        
        self.print_section("Security & Authentication")
        print("  🔐 JWT-based authentication")
        print("  👥 Role-based access control")
        print("  🛡️  Data encryption in transit")
        print("  🔒 Secure password hashing")
        print("  📝 Audit logging")
        
        self.print_section("Analytics & Reporting")
        print("  📈 Performance dashboards")
        print("  📊 Customer satisfaction tracking")
        print("  ⏱️  Service time analytics")
        print("  🎯 KPI monitoring")
        print("  📋 Custom reports")
    
    def run_demo(self):
        """Run the complete demo"""
        print("🚀 ISP TECHNICIAN ROUTING SYSTEM")
        print("   Smart AI-Powered Field Service Management")
        print("   Similar to Uber/Grab but for ISP Technicians")
        
        # Demo each view
        self.demo_admin_view()
        time.sleep(2)
        
        self.demo_technician_view()
        time.sleep(2)
        
        self.demo_customer_view()
        time.sleep(2)
        
        self.demo_system_features()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("\n🎯 Key Benefits Demonstrated:")
        print("  • Automated job assignment and routing")
        print("  • Real-time tracking and communication")
        print("  • Multi-platform user interfaces")
        print("  • Comprehensive admin management")
        print("  • Customer transparency and satisfaction")
        
        print("\n🚀 Ready for Production:")
        print("  • Backend API: Python Flask with MongoDB")
        print("  • Mobile App: React Native with Expo")
        print("  • Web Portal: React with Material-UI")
        print("  • Security: JWT authentication & role-based access")
        print("  • Deployment: Docker containers with CI/CD")
        print("="*60)

if __name__ == "__main__":
    demo = MockDemo()
    demo.run_demo()
