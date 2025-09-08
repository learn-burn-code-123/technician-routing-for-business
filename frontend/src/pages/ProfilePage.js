import React, { useState, useEffect, useContext } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  TextField, 
  Button, 
  Divider, 
  CircularProgress, 
  Alert, 
  Card,
  CardContent,
  Avatar
} from '@mui/material';
import { 
  Person as PersonIcon,
  Save as SaveIcon,
  Edit as EditIcon
} from '@mui/icons-material';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

const ProfilePage = () => {
  const { user } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: ''
  });

  // Load profile when component mounts
  useEffect(() => {
    fetchProfile();
  }, []);

  // Fetch profile from API
  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get customer profile
      const response = await api.customer.getProfile();
      setProfile(response.data);
      
      // Initialize form data
      setFormData({
        name: response.data.name || '',
        email: response.data.email || '',
        phone: response.data.phone || '',
        address: response.data.address || ''
      });
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load profile. Please try again.');
      setLoading(false);
      console.error('Error fetching profile:', err);
    }
  };

  // Handle form input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Toggle edit mode
  const toggleEditMode = () => {
    if (editMode) {
      // Reset form data when canceling edit
      setFormData({
        name: profile.name || '',
        email: profile.email || '',
        phone: profile.phone || '',
        address: profile.address || ''
      });
    }
    setEditMode(!editMode);
    setSuccess(null);
  };

  // Save profile changes
  const handleSaveProfile = async (e) => {
    e.preventDefault();
    
    try {
      setSaving(true);
      setError(null);
      setSuccess(null);
      
      // Update profile
      await api.customer.updateProfile(formData);
      
      // Refresh profile data
      const response = await api.customer.getProfile();
      setProfile(response.data);
      
      setSuccess('Profile updated successfully.');
      setEditMode(false);
      setSaving(false);
    } catch (err) {
      setError('Failed to update profile. Please try again.');
      setSaving(false);
      console.error('Error updating profile:', err);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Profile
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          {success}
        </Alert>
      )}
      
      <Grid container spacing={3}>
        {/* Profile Summary */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Avatar 
                sx={{ width: 100, height: 100, mx: 'auto', mb: 2 }}
                alt={profile?.name || user?.name || 'User'}
              >
                <PersonIcon sx={{ fontSize: 60 }} />
              </Avatar>
              
              <Typography variant="h5" gutterBottom>
                {profile?.name || user?.name || 'Customer'}
              </Typography>
              
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Account ID: {profile?._id?.substring(0, 8) || user?.customer_id?.substring(0, 8) || 'N/A'}
              </Typography>
              
              <Typography variant="body2" color="text.secondary">
                Service Tier: {profile?.service_tier || 'Standard'}
              </Typography>
              
              <Button
                variant={editMode ? "outlined" : "contained"}
                startIcon={editMode ? null : <EditIcon />}
                onClick={toggleEditMode}
                sx={{ mt: 3 }}
              >
                {editMode ? 'Cancel' : 'Edit Profile'}
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Profile Details */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              {editMode ? 'Edit Profile Information' : 'Profile Information'}
            </Typography>
            
            <Divider sx={{ mb: 3 }} />
            
            <Box component="form" onSubmit={handleSaveProfile}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Full Name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    disabled={!editMode || saving}
                    required
                  />
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Email Address"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    disabled={!editMode || saving}
                    required
                  />
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Phone Number"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    disabled={!editMode || saving}
                    required
                  />
                </Grid>
                
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Address"
                    name="address"
                    value={formData.address}
                    onChange={handleInputChange}
                    disabled={!editMode || saving}
                    multiline
                    rows={2}
                    required
                  />
                </Grid>
                
                {editMode && (
                  <Grid item xs={12}>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      startIcon={<SaveIcon />}
                      disabled={saving}
                      sx={{ mt: 1 }}
                    >
                      {saving ? <CircularProgress size={24} /> : 'Save Changes'}
                    </Button>
                  </Grid>
                )}
              </Grid>
            </Box>
          </Paper>
          
          {/* Account Information */}
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Account Information
            </Typography>
            
            <Divider sx={{ mb: 3 }} />
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Account ID
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {profile?._id || 'N/A'}
                </Typography>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Service Tier
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {profile?.service_tier || 'Standard'}
                </Typography>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Customer Since
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {profile?.created_at 
                    ? new Date(profile.created_at).toLocaleDateString() 
                    : 'N/A'}
                </Typography>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Last Updated
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {profile?.updated_at 
                    ? new Date(profile.updated_at).toLocaleDateString() 
                    : 'N/A'}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProfilePage;
