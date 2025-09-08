import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Box, 
  Typography, 
  Paper, 
  Tabs, 
  Tab, 
  Card, 
  CardContent, 
  CardActions, 
  Button, 
  Chip, 
  Grid, 
  CircularProgress, 
  Alert,
  TextField,
  InputAdornment,
  IconButton
} from '@mui/material';
import { 
  Search as SearchIcon,
  Event as EventIcon,
  Schedule as ScheduleIcon,
  Person as PersonIcon,
  LocationOn as LocationIcon,
  Clear as ClearIcon
} from '@mui/icons-material';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

const AppointmentsPage = () => {
  const [appointments, setAppointments] = useState([]);
  const [filteredAppointments, setFilteredAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
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

  // Tab labels and values
  const tabs = [
    { label: 'All', value: 'all' },
    { label: 'Upcoming', value: 'upcoming' },
    { label: 'Completed', value: 'completed' },
    { label: 'Cancelled', value: 'cancelled' }
  ];

  // Load appointments when component mounts
  useEffect(() => {
    fetchAppointments();
  }, []);

  // Filter appointments when tab or search query changes
  useEffect(() => {
    filterAppointments();
  }, [tabValue, searchQuery, appointments]);

  // Fetch appointments from API
  const fetchAppointments = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get appointments for the customer
      const response = await api.jobs.getJobs({ 
        customer_id: user?.customer_id
      });
      
      setAppointments(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load appointments. Please try again.');
      setLoading(false);
      console.error('Error fetching appointments:', err);
    }
  };

  // Filter appointments based on tab and search query
  const filterAppointments = () => {
    if (!appointments.length) {
      setFilteredAppointments([]);
      return;
    }
    
    // Get the selected tab value
    const selectedTab = tabs[tabValue].value;
    
    // Filter by tab
    let filtered = appointments;
    if (selectedTab === 'upcoming') {
      filtered = appointments.filter(appointment => 
        ['pending', 'assigned', 'in_progress'].includes(appointment.status)
      );
    } else if (selectedTab === 'completed') {
      filtered = appointments.filter(appointment => 
        appointment.status === 'completed'
      );
    } else if (selectedTab === 'cancelled') {
      filtered = appointments.filter(appointment => 
        appointment.status === 'cancelled'
      );
    }
    
    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(appointment => 
        appointment.service_type.toLowerCase().includes(query) ||
        appointment._id.toLowerCase().includes(query) ||
        (appointment.location?.address && appointment.location.address.toLowerCase().includes(query)) ||
        (appointment.technician_name && appointment.technician_name.toLowerCase().includes(query))
      );
    }
    
    // Sort by date (most recent first)
    filtered.sort((a, b) => {
      return new Date(b.scheduled_date) - new Date(a.scheduled_date);
    });
    
    setFilteredAppointments(filtered);
  };

  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  // Handle search query change
  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  // Clear search query
  const handleClearSearch = () => {
    setSearchQuery('');
  };

  // Navigate to appointment details
  const handleViewAppointment = (appointmentId) => {
    navigate(`/appointments/${appointmentId}`);
  };

  // Format date for display
  const formatDate = (dateString) => {
    const options = { weekday: 'short', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Appointments
      </Typography>
      
      <Paper sx={{ mb: 3 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            aria-label="appointment tabs"
            variant="scrollable"
            scrollButtons="auto"
          >
            {tabs.map((tab, index) => (
              <Tab key={tab.value} label={tab.label} id={`tab-${index}`} />
            ))}
          </Tabs>
        </Box>
        
        <Box sx={{ p: 2 }}>
          <TextField
            fullWidth
            placeholder="Search appointments..."
            value={searchQuery}
            onChange={handleSearchChange}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
              endAdornment: searchQuery && (
                <InputAdornment position="end">
                  <IconButton onClick={handleClearSearch} edge="end">
                    <ClearIcon />
                  </IconButton>
                </InputAdornment>
              )
            }}
            variant="outlined"
            size="small"
            sx={{ mb: 2 }}
          />
          
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress />
            </Box>
          ) : error ? (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
              <Button 
                color="inherit" 
                size="small" 
                onClick={fetchAppointments}
                sx={{ ml: 2 }}
              >
                Retry
              </Button>
            </Alert>
          ) : filteredAppointments.length === 0 ? (
            <Box sx={{ textAlign: 'center', p: 3 }}>
              <Typography variant="body1" color="text.secondary">
                {searchQuery 
                  ? 'No appointments match your search.' 
                  : `No ${tabs[tabValue].value !== 'all' ? tabs[tabValue].label.toLowerCase() : ''} appointments found.`}
              </Typography>
            </Box>
          ) : (
            <Grid container spacing={2}>
              {filteredAppointments.map((appointment) => (
                <Grid item xs={12} sm={6} md={4} key={appointment._id}>
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
                        <EventIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                        {formatDate(appointment.scheduled_date)}
                      </Typography>
                      
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                        <ScheduleIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                        {appointment.scheduled_time_window?.start} - {appointment.scheduled_time_window?.end}
                      </Typography>
                      
                      {appointment.location?.address && (
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                          <LocationIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                          {appointment.location.address}
                        </Typography>
                      )}
                      
                      {appointment.technician_name && (
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                          <PersonIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                          {appointment.technician_name}
                        </Typography>
                      )}
                      
                      {appointment.estimated_arrival_time && (
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                          <ScheduleIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                          ETA: {appointment.estimated_arrival_time}
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
        </Box>
      </Paper>
    </Box>
  );
};

export default AppointmentsPage;
