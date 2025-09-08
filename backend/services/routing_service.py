import os
import requests
from datetime import datetime, timedelta
from haversine import haversine
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from services.job_service import JobService
from services.technician_service import TechnicianService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RoutingService:
    """Service for optimizing technician routes"""
    
    def __init__(self):
        self.job_service = JobService()
        self.technician_service = TechnicianService()
        self.google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    def optimize_routes_for_date(self, date, technician_ids=None, consider_traffic=True, consider_weather=True):
        """Optimize routes for technicians on a specific date"""
        try:
            # Get all jobs for the date
            jobs = self.job_service.get_all_jobs(date=date, status="pending")
            
            # If no jobs, return empty result
            if not jobs:
                return {"routes": [], "metrics": {"total_jobs": 0, "assigned_jobs": 0}}
            
            # Get available technicians
            if technician_ids:
                technicians = [self.technician_service.get_technician_by_id(tech_id) for tech_id in technician_ids]
                technicians = [tech for tech in technicians if tech and tech.get('status') == 'available']
            else:
                technicians = self.technician_service.get_all_technicians(status="available")
            
            # If no technicians, return empty result
            if not technicians:
                return {"routes": [], "metrics": {"total_jobs": len(jobs), "assigned_jobs": 0}}
            
            # Build distance matrix
            distance_matrix, locations = self._build_distance_matrix(jobs, technicians, consider_traffic)
            
            # Create data model for OR-Tools
            data = self._create_data_model(distance_matrix, jobs, technicians)
            
            # Solve the VRP problem
            solution = self._solve_vrp(data)
            
            # Process solution
            routes = self._process_solution(solution, data, jobs, technicians, locations)
            
            # Assign jobs to technicians based on the solution
            assigned_jobs = self._assign_jobs_to_technicians(routes)
            
            # Return the optimized routes and metrics
            return {
                "routes": routes,
                "metrics": {
                    "total_jobs": len(jobs),
                    "assigned_jobs": assigned_jobs
                }
            }
            
        except Exception as e:
            print(f"Error optimizing routes: {e}")
            raise
    
    def _build_distance_matrix(self, jobs, technicians, consider_traffic=True):
        """Build distance matrix between all locations"""
        # Collect all locations (technician starting points + job locations)
        locations = []
        
        # Add technician starting locations
        for tech in technicians:
            if tech.get('current_location'):
                locations.append(tech['current_location'])
            elif tech.get('location'):
                locations.append(tech['location'])
            else:
                # Default location if none provided
                locations.append({"lat": 0, "lng": 0})
        
        # Add job locations
        for job in jobs:
            locations.append(job['location'])
        
        # Initialize distance matrix
        n = len(locations)
        distance_matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        # If Google Maps API key is available, use Distance Matrix API
        if self.google_maps_api_key:
            try:
                # Build distance matrix using Google Maps API
                for i in range(n):
                    for j in range(i+1, n):
                        if i != j:
                            origin = f"{locations[i]['lat']},{locations[i]['lng']}"
                            destination = f"{locations[j]['lat']},{locations[j]['lng']}"
                            
                            # API parameters
                            params = {
                                "origins": origin,
                                "destinations": destination,
                                "key": self.google_maps_api_key
                            }
                            
                            if consider_traffic:
                                params["departure_time"] = "now"
                                params["traffic_model"] = "best_guess"
                            
                            # Make API request
                            response = requests.get(
                                "https://maps.googleapis.com/maps/api/distancematrix/json",
                                params=params
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                if result["status"] == "OK":
                                    # Get duration in seconds
                                    duration = result["rows"][0]["elements"][0]["duration"]["value"]
                                    
                                    # If traffic info is available
                                    if consider_traffic and "duration_in_traffic" in result["rows"][0]["elements"][0]:
                                        duration = result["rows"][0]["elements"][0]["duration_in_traffic"]["value"]
                                    
                                    # Convert to minutes and round
                                    duration_minutes = round(duration / 60)
                                    
                                    # Update distance matrix (symmetric)
                                    distance_matrix[i][j] = duration_minutes
                                    distance_matrix[j][i] = duration_minutes
            except Exception as e:
                print(f"Error using Google Maps API: {e}")
                # Fall back to haversine distance
                self._build_haversine_distance_matrix(distance_matrix, locations)
        else:
            # Use haversine distance if no API key
            self._build_haversine_distance_matrix(distance_matrix, locations)
        
        return distance_matrix, locations
    
    def _build_haversine_distance_matrix(self, distance_matrix, locations):
        """Build distance matrix using haversine formula"""
        n = len(locations)
        for i in range(n):
            for j in range(i+1, n):
                if i != j:
                    # Calculate haversine distance
                    point1 = (locations[i]['lat'], locations[i]['lng'])
                    point2 = (locations[j]['lat'], locations[j]['lng'])
                    
                    # Get distance in km
                    distance_km = haversine(point1, point2)
                    
                    # Estimate time in minutes (assuming 40 km/h average speed)
                    time_minutes = round(distance_km / 40 * 60)
                    
                    # Update distance matrix (symmetric)
                    distance_matrix[i][j] = time_minutes
                    distance_matrix[j][i] = time_minutes
    
    def _create_data_model(self, distance_matrix, jobs, technicians):
        """Create data model for OR-Tools VRP solver"""
        data = {}
        data['distance_matrix'] = distance_matrix
        data['num_vehicles'] = len(technicians)
        data['depot'] = 0  # Start from the first location (technician's location)
        
        # Time windows for each location
        data['time_windows'] = []
        
        # Add time windows for technician starting points (depot)
        for tech in technicians:
            # Default working hours if not specified
            working_hours = tech.get('working_hours', {})
            today_name = datetime.now().strftime('%A').lower()
            
            if today_name in working_hours and working_hours[today_name]:
                start_time = self._time_to_minutes(working_hours[today_name]['start'])
                end_time = self._time_to_minutes(working_hours[today_name]['end'])
            else:
                # Default: 9 AM to 5 PM
                start_time = 9 * 60
                end_time = 17 * 60
            
            data['time_windows'].append((start_time, end_time))
        
        # Add time windows for jobs
        for job in jobs:
            time_window = job.get('scheduled_time_window', {"start": "09:00", "end": "17:00"})
            start_time = self._time_to_minutes(time_window['start'])
            end_time = self._time_to_minutes(time_window['end'])
            data['time_windows'].append((start_time, end_time))
        
        # Service times (duration) for each location
        data['service_times'] = [0] * len(technicians)  # No service time for technician starting points
        for job in jobs:
            # Get estimated duration in minutes, default to 60 minutes
            duration = job.get('estimated_duration', 60)
            data['service_times'].append(duration)
        
        # Vehicle capacities (skills matching)
        data['vehicle_capacities'] = [1] * len(technicians)  # Default capacity
        
        # Job requirements (skills needed)
        data['job_requirements'] = [0] * len(technicians)  # No requirements for technician starting points
        for job in jobs:
            # For simplicity, we're using a binary skill match
            # In a real system, this would be more complex
            data['job_requirements'].append(1)  # All jobs require skill level 1
        
        return data
    
    def _solve_vrp(self, data):
        """Solve the Vehicle Routing Problem using OR-Tools"""
        # Create the routing index manager
        manager = pywrapcp.RoutingIndexManager(
            len(data['distance_matrix']),
            data['num_vehicles'],
            data['depot']
        )
        
        # Create Routing Model
        routing = pywrapcp.RoutingModel(manager)
        
        # Define transit callback
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]
        
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        
        # Define cost of each arc
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        # Add Time Windows constraint
        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node] + data['service_times'][from_node]
        
        time_callback_index = routing.RegisterTransitCallback(time_callback)
        
        # Add time window constraints
        routing.AddDimension(
            time_callback_index,
            30,  # Allow waiting time
            480,  # Maximum time per vehicle (8 hours)
            False,  # Don't force start cumul to zero
            'Time'
        )
        time_dimension = routing.GetDimensionOrDie('Time')
        
        # Add time window constraints for each location
        for location_idx, time_window in enumerate(data['time_windows']):
            if location_idx == data['depot']:
                continue  # Skip depot
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        
        # Add resource constraints (skills)
        # This is a simplified version; in a real system, this would be more complex
        
        # Setting first solution heuristic
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = 30  # Limit solution time
        
        # Solve the problem
        solution = routing.SolveWithParameters(search_parameters)
        
        return solution
    
    def _process_solution(self, solution, data, jobs, technicians, locations):
        """Process the solution from OR-Tools"""
        routes = []
        
        if not solution:
            return routes
        
        # Get the routing model
        manager = solution.routing_index_manager
        routing = solution.routing_model
        time_dimension = routing.GetDimensionOrDie('Time')
        
        # Process each vehicle route
        for vehicle_id in range(data['num_vehicles']):
            route = {
                "technician_id": technicians[vehicle_id]['_id'],
                "technician_name": technicians[vehicle_id]['name'],
                "jobs": []
            }
            
            index = routing.Start(vehicle_id)
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                
                # Skip the depot (technician starting point)
                if node_index >= len(technicians):
                    job_index = node_index - len(technicians)
                    job = jobs[job_index]
                    
                    # Get the time window
                    time_var = time_dimension.CumulVar(index)
                    arrival_time = solution.Min(time_var)
                    departure_time = arrival_time + job.get('estimated_duration', 60)
                    
                    # Format times
                    arrival_time_str = self._minutes_to_time(arrival_time)
                    departure_time_str = self._minutes_to_time(departure_time)
                    
                    # Add job to route
                    route["jobs"].append({
                        "job_id": job['_id'],
                        "customer_id": job['customer_id'],
                        "service_type": job['service_type'],
                        "location": job['location'],
                        "estimated_arrival_time": arrival_time_str,
                        "estimated_departure_time": departure_time_str,
                        "estimated_duration": job.get('estimated_duration', 60)
                    })
                
                index = solution.Value(routing.NextVar(index))
            
            # Only add routes with jobs
            if route["jobs"]:
                routes.append(route)
        
        return routes
    
    def _assign_jobs_to_technicians(self, routes):
        """Assign jobs to technicians based on the optimized routes"""
        assigned_jobs = 0
        
        for route in routes:
            technician_id = route["technician_id"]
            
            for job_info in route["jobs"]:
                job_id = job_info["job_id"]
                
                # Update job with technician assignment and estimated times
                update_data = {
                    "technician_id": technician_id,
                    "status": "assigned",
                    "estimated_arrival_time": job_info["estimated_arrival_time"],
                    "estimated_departure_time": job_info["estimated_departure_time"]
                }
                
                success = self.job_service.update_job(job_id, update_data)
                if success:
                    assigned_jobs += 1
        
        return assigned_jobs
    
    def _time_to_minutes(self, time_str):
        """Convert time string (HH:MM) to minutes since midnight"""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    def _minutes_to_time(self, minutes):
        """Convert minutes since midnight to time string (HH:MM)"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
