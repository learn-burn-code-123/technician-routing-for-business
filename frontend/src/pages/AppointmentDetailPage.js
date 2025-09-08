import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Chip, 
  Divider, 
  Button, 
  CircularProgress, 
  Alert,
  Card,
  CardContent,
  CardMedia,
  Avatar,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import { 
  Event as EventIcon,
  Schedule as ScheduleIcon,
  LocationOn as LocationIcon,
  Person as PersonIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  Build as BuildIcon,
  Notes as NotesIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import api from '../services/api';

const AppointmentDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [appointment, setAppointment] = useState(null);
  const [technician, setTechnician] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Status colors for visual indication
  const statusColors = {
    pending: 'warning',
    assigned: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'error'
  };

  // Load appointment details when component mounts
  useEffect(() => {
    fetchAppointmentDetails();
  }, [id]);

  // Fetch appointment details from API
  const fetchAppointmentDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get appointment details
      const appointmentResponse = await api.jobs.getJobById(id);
      setAppointment(appointmentResponse.data);
      
      // If technician is assigned, get technician details
      if (appointmentResponse.data.technician_id) {
        try {
          const technicianResponse = await api.technician.getTechnicianById(
            appointmentResponse.data.technician_id
          );
          setTechnician(technicianResponse.data);
        } catch (techErr) {
          console.error('Error fetching technician details:', techErr);
          // Don't set error state here, as we still have the appointment data
        }
      }
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load appointment details. Please try again.');
      setLoading(false);
      console.error('Error fetching appointment details:', err);
    }
  };

  // Format date for display
  const formatDate = (dateString) => {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  // Get status label
  const getStatusLabel = (status) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  // Go back to appointments list
  const handleGoBack = () => {
    navigate('/appointments');
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert 
          severity="error" 
          action={
            <Button color="inherit" size="small" onClick={fetchAppointmentDetails}>
              Retry
            </Button>
          }
        >
          {error}
        </Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleGoBack}
          sx={{ mt: 2 }}
        >
          Back to Appointments
        </Button>
      </Box>
    );
  }

  if (!appointment) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="warning">Appointment not found.</Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleGoBack}
          sx={{ mt: 2 }}
        >
          Back to Appointments
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={handleGoBack}
        sx={{ mb: 2 }}
      >
        Back to Appointments
      </Button>
      
      <Typography variant="h4" gutterBottom>
        Appointment Details
      </Typography>
      
      <Grid container spacing={3}>
        {/* Appointment Details */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" component="h2">
                {appointment.service_type}
              </Typography>
              <Chip 
                label={getStatusLabel(appointment.status)} 
                color={statusColors[appointment.status] || 'default'} 
              />
            </Box>
            
            <Divider sx={{ mb: 2 }} />
            
            <List>
              <ListItem>
                <ListItemIcon>
                  <EventIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Date" 
                  secondary={formatDate(appointment.scheduled_date)} 
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  <ScheduleIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Time Window" 
                  secondary={`${appointment.scheduled_time_window?.start} - ${appointment.scheduled_time_window?.end}`} 
                />
              </ListItem>
              
              {appointment.estimated_arrival_time && (
                <ListItem>
                  <ListItemIcon>
                    <ScheduleIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Estimated Arrival Time" 
                    secondary={appointment.estimated_arrival_time} 
                  />
                </ListItem>
              )}
              
              <ListItem>
                <ListItemIcon>
                  <LocationIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Location" 
                  secondary={appointment.location?.address || 'No address provided'} 
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  <BuildIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Service Type" 
                  secondary={appointment.service_type} 
                />
              </ListItem>
              
              {appointment.notes && (
                <ListItem>
                  <ListItemIcon>
                    <NotesIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Notes" 
                    secondary={appointment.notes} 
                  />
                </ListItem>
              )}
            </List>
            
            {appointment.status === 'in_progress' && (
              <Alert severity="info" sx={{ mt: 2 }}>
                Your technician is currently working on this service.
              </Alert>
            )}
            
            {appointment.status === 'pending' && !appointment.technician_id && (
              <Alert severity="info" sx={{ mt: 2 }}>
                A technician has not yet been assigned to this appointment.
              </Alert>
            )}
          </Paper>
        </Grid>
        
        {/* Technician Information */}
        <Grid item xs={12} md={4}>
          {technician ? (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Assigned Technician
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar 
                    sx={{ width: 64, height: 64, mr: 2 }}
                    alt={technician.name}
                  >
                    {technician.name?.charAt(0) || 'T'}
                  </Avatar>
                  <Box>
                    <Typography variant="h6">
                      {technician.name}
                    </Typography>
                    <Chip 
                      label={technician.status === 'available' ? 'Available' : 'Busy'} 
                      color={technician.status === 'available' ? 'success' : 'warning'} 
                      size="small" 
                    />
                  </Box>
                </Box>
                
                <Divider sx={{ mb: 2 }} />
                
                <List dense>
                  {technician.phone && (
                    <ListItem>
                      <ListItemIcon>
                        <PhoneIcon fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={technician.phone} />
                    </ListItem>
                  )}
                  
                  {technician.email && (
                    <ListItem>
                      <ListItemIcon>
                        <EmailIcon fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={technician.email} />
                    </ListItem>
                  )}
                </List>
                
                {technician.skills && technician.skills.length > 0 && (
                  <>
                    <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
                      Skills & Certifications
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {technician.skills.map((skill, index) => (
                        <Chip key={index} label={skill} size="small" />
                      ))}
                    </Box>
                  </>
                )}
              </CardContent>
            </Card>
          ) : appointment.status !== 'pending' ? (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Technician Information
              </Typography>
              <Alert severity="info">
                Technician details are not available at this moment.
              </Alert>
            </Paper>
          ) : null}
          
          {/* Appointment Status Card */}
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Appointment Status
            </Typography>
            
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Current Status
              </Typography>
              <Chip 
                label={getStatusLabel(appointment.status)} 
                color={statusColors[appointment.status] || 'default'} 
              />
            </Box>
            
            {appointment.status === 'completed' && appointment.actual_end_time && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Completed At
                </Typography>
                <Typography variant="body1">
                  {new Date(appointment.actual_end_time).toLocaleString()}
                </Typography>
              </Box>
            )}
            
            {appointment.status === 'cancelled' && (
              <Alert severity="warning" sx={{ mt: 2 }}>
                This appointment has been cancelled.
              </Alert>
            )}
            
            {appointment.status === 'assigned' && (
              <Alert severity="info" sx={{ mt: 2 }}>
                A technician has been assigned and will arrive during the scheduled time window.
              </Alert>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AppointmentDetailPage;
