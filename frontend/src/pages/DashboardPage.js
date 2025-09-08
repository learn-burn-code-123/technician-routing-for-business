import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Card, 
  CardContent, 
  CardActions, 
  Button, 
  Divider, 
  Chip, 
  CircularProgress, 
  Alert 
} from '@mui/material';
import { 
  Event as EventIcon, 
  Schedule as ScheduleIcon, 
  Person as PersonIcon, 
  Build as BuildIcon 
} from '@mui/icons-material';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

const DashboardPage = () => {
  const [upcomingAppointments, setUpcomingAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  // Status colors for visual indication
  const statusColors = {
    pending: 'warning',
    assigned: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'error'
  };

  // Load upcoming appointments when component mounts
  useEffect(() => {
    fetchUpcomingAppointments();
  }, []);

  // Fetch upcoming appointments from API
  const fetchUpcomingAppointments = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get current date in YYYY-MM-DD format
      const today = new Date().toISOString().split('T')[0];
      
      // Get upcoming appointments
      const response = await api.jobs.getJobs({ 
        customer_id: user?.customer_id,
        start_date: today,
        limit: 3
      });
      
      setUpcomingAppointments(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load upcoming appointments. Please try again.');
      setLoading(false);
      console.error('Error fetching appointments:', err);
    }
  };

  // Navigate to appointment details
  const handleViewAppointment = (appointmentId) => {
    navigate(`/appointments/${appointmentId}`);
  };

  // Navigate to all appointments
  const handleViewAllAppointments = () => {
    navigate('/appointments');
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome, {user?.name || 'Customer'}
      </Typography>
      
      <Grid container spacing={3}>
        {/* Upcoming Appointments Section */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" component="h2">
                <EventIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Upcoming Appointments
              </Typography>
              <Button 
                variant="outlined" 
                size="small" 
                onClick={handleViewAllAppointments}
              >
                View All
              </Button>
            </Box>
            
            <Divider sx={{ mb: 2 }} />
            
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                <CircularProgress />
              </Box>
            ) : error ? (
              <Alert severity="error">{error}</Alert>
            ) : upcomingAppointments.length === 0 ? (
              <Box sx={{ textAlign: 'center', p: 3 }}>
                <Typography variant="body1" color="text.secondary">
                  You have no upcoming appointments.
                </Typography>
              </Box>
            ) : (
              <Grid container spacing={2}>
                {upcomingAppointments.map((appointment) => (
                  <Grid item xs={12} key={appointment._id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                          <Typography variant="h6" component="div">
                            {appointment.service_type}
                          </Typography>
                          <Chip 
                            label={appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)} 
                            color={statusColors[appointment.status] || 'default'} 
                            size="small" 
                          />
                        </Box>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                          <ScheduleIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                          {appointment.scheduled_date} | {appointment.scheduled_time_window?.start} - {appointment.scheduled_time_window?.end}
                        </Typography>
                        
                        {appointment.technician_id && appointment.technician_name && (
                          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                            <PersonIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                            Technician: {appointment.technician_name}
                          </Typography>
                        )}
                        
                        {appointment.estimated_arrival_time && (
                          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                            <ScheduleIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                            Estimated arrival: {appointment.estimated_arrival_time}
                          </Typography>
                        )}
                      </CardContent>
                      <CardActions>
                        <Button 
                          size="small" 
                          onClick={() => handleViewAppointment(appointment._id)}
                        >
                          View Details
                        </Button>
                      </CardActions>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </Paper>
        </Grid>
        
        {/* Quick Info Section */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" component="h2" gutterBottom>
              Quick Info
            </Typography>
            
            <Divider sx={{ mb: 2 }} />
            
            <Card variant="outlined" sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" component="div">
                  <PersonIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Account Information
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  Account Number: {user?.customer_id?.substring(0, 8) || 'N/A'}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                  Service Tier: {user?.service_tier || 'Standard'}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => navigate('/profile')}>
                  View Profile
                </Button>
              </CardActions>
            </Card>
            
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" component="div">
                  <BuildIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Need Help?
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  Contact our customer support for assistance with your service.
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary">
                  Contact Support
                </Button>
              </CardActions>
            </Card>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;
