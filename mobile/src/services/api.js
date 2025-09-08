import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Create axios instance
const api = axios.create({
  baseURL: 'http://192.168.1.100:5000/api/v1', // Replace with your actual API URL
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000
});

// Add request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('userToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // Handle 401 Unauthorized errors (token expired)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      // Clear stored tokens and user info
      await AsyncStorage.removeItem('userToken');
      await AsyncStorage.removeItem('userInfo');
      
      // Redirect to login (this will be handled by the navigation)
      // The auth context will detect the missing token on next app load
      
      return Promise.reject(error);
    }
    
    return Promise.reject(error);
  }
);

// Job API calls
const jobApi = {
  getJobs: (filters = {}) => {
    return api.get('/jobs', { params: filters });
  },
  
  getJobById: (jobId) => {
    return api.get(`/jobs/${jobId}`);
  },
  
  updateJobStatus: (jobId, status, data = {}) => {
    return api.put(`/jobs/${jobId}`, { 
      status,
      ...data
    });
  },
  
  startJob: (jobId) => {
    return api.put(`/jobs/${jobId}`, { 
      status: 'in_progress',
      actual_start_time: new Date().toISOString()
    });
  },
  
  completeJob: (jobId, notes = '') => {
    return api.put(`/jobs/${jobId}`, { 
      status: 'completed',
      actual_end_time: new Date().toISOString(),
      notes
    });
  }
};

// Technician API calls
const technicianApi = {
  getTechnicianProfile: () => {
    return api.get('/technicians/profile');
  },
  
  updateLocation: (location) => {
    return api.put('/technicians/location', { location });
  },
  
  updateStatus: (status) => {
    return api.put('/technicians/status', { status });
  }
};

// Customer API calls
const customerApi = {
  getCustomerById: (customerId) => {
    return api.get(`/customers/${customerId}`);
  }
};

export default {
  ...api,
  job: jobApi,
  technician: technicianApi,
  customer: customerApi
};
