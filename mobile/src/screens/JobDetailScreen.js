import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert, Linking } from 'react-native';
import { 
  Card, 
  Title, 
  Paragraph, 
  Button, 
  ActivityIndicator, 
  Text,
  Chip,
  Divider,
  TextInput,
  Portal,
  Dialog,
  IconButton
} from 'react-native-paper';
import { useRoute, useNavigation } from '@react-navigation/native';
import api from '../services/api';
import * as Location from 'expo-location';

const JobDetailScreen = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const { jobId } = route.params;
  
  const [job, setJob] = useState(null);
  const [customer, setCustomer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [completionNotes, setCompletionNotes] = useState('');
  const [dialogVisible, setDialogVisible] = useState(false);
  
  // Status colors for visual indication
  const statusColors = {
    pending: '#FFC107',
    assigned: '#2196F3',
    in_progress: '#FF9800',
    completed: '#4CAF50',
    cancelled: '#F44336'
  };

  // Fetch job details when screen loads
  useEffect(() => {
    fetchJobDetails();
  }, [jobId]);

  // Fetch job details from API
  const fetchJobDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get job details
      const jobResponse = await api.job.getJobById(jobId);
      setJob(jobResponse.data);
      
      // Get customer details
      if (jobResponse.data.customer_id) {
        const customerResponse = await api.customer.getCustomerById(jobResponse.data.customer_id);
        setCustomer(customerResponse.data);
      }
    } catch (err) {
      setError('Failed to load job details. Please try again.');
      console.error('Error fetching job details:', err);
    } finally {
      setLoading(false);
    }
  };

  // Start job
  const handleStartJob = async () => {
    try {
      await api.job.startJob(jobId);
      fetchJobDetails(); // Refresh job details
    } catch (err) {
      Alert.alert('Error', 'Failed to start job. Please try again.');
      console.error('Error starting job:', err);
    }
  };

  // Complete job
  const handleCompleteJob = async () => {
    try {
      await api.job.completeJob(jobId, completionNotes);
      setDialogVisible(false);
      fetchJobDetails(); // Refresh job details
    } catch (err) {
      Alert.alert('Error', 'Failed to complete job. Please try again.');
      console.error('Error completing job:', err);
    }
  };

  // Update technician location
  const updateLocation = async () => {
    try {
      // Request location permission
      const { status } = await Location.requestForegroundPermissionsAsync();
      
      if (status !== 'granted') {
        Alert.alert('Permission Denied', 'Location permission is required to update your location.');
        return;
      }
      
      // Get current location
      const location = await Location.getCurrentPositionAsync({});
      const { latitude, longitude } = location.coords;
      
      // Update technician location
      await api.technician.updateLocation({
        lat: latitude,
        lng: longitude
      });
      
      Alert.alert('Success', 'Your location has been updated.');
    } catch (err) {
      Alert.alert('Error', 'Failed to update location. Please try again.');
      console.error('Error updating location:', err);
    }
  };

  // Open maps app for navigation
  const openMapsNavigation = () => {
    if (!job?.location?.lat || !job?.location?.lng) {
      Alert.alert('Error', 'Location coordinates not available for this job.');
      return;
    }
    
    const { lat, lng } = job.location;
    const url = Platform.select({
      ios: `maps:${lat},${lng}`,
      android: `geo:${lat},${lng}?q=${lat},${lng}`
    });
    
    Linking.canOpenURL(url)
      .then(supported => {
        if (supported) {
          return Linking.openURL(url);
        } else {
          const browserUrl = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
          return Linking.openURL(browserUrl);
        }
      })
      .catch(err => {
        Alert.alert('Error', 'Could not open maps application.');
        console.error('Error opening maps:', err);
      });
  };

  // Make a phone call
  const makePhoneCall = (phoneNumber) => {
    if (!phoneNumber) {
      Alert.alert('Error', 'Phone number not available.');
      return;
    }
    
    const url = `tel:${phoneNumber}`;
    
    Linking.canOpenURL(url)
      .then(supported => {
        if (supported) {
          return Linking.openURL(url);
        } else {
          Alert.alert('Error', 'Phone calls are not supported on this device.');
        }
      })
      .catch(err => {
        Alert.alert('Error', 'Could not make phone call.');
        console.error('Error making phone call:', err);
      });
  };

  // Send an email
  const sendEmail = (email) => {
    if (!email) {
      Alert.alert('Error', 'Email address not available.');
      return;
    }
    
    const url = `mailto:${email}`;
    
    Linking.canOpenURL(url)
      .then(supported => {
        if (supported) {
          return Linking.openURL(url);
        } else {
          Alert.alert('Error', 'Email is not supported on this device.');
        }
      })
      .catch(err => {
        Alert.alert('Error', 'Could not send email.');
        console.error('Error sending email:', err);
      });
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0066cc" />
        <Text style={styles.loadingText}>Loading job details...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{error}</Text>
        <Button mode="contained" onPress={fetchJobDetails}>
          Retry
        </Button>
      </View>
    );
  }

  if (!job) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Job not found</Text>
        <Button mode="contained" onPress={() => navigation.goBack()}>
          Go Back
        </Button>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Job Status Card */}
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.cardHeader}>
            <Title>Job #{job._id.substring(0, 8)}</Title>
            <Chip 
              style={[styles.statusChip, { backgroundColor: statusColors[job.status] || '#999' }]}
              textStyle={{ color: '#fff' }}
            >
              {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
            </Chip>
          </View>
          
          <Paragraph style={styles.serviceType}>
            {job.service_type.toUpperCase()}
          </Paragraph>
          
          <Divider style={styles.divider} />
          
          <View style={styles.detailRow}>
            <Text style={styles.label}>Scheduled Date:</Text>
            <Text>{job.scheduled_date}</Text>
          </View>
          
          <View style={styles.detailRow}>
            <Text style={styles.label}>Time Window:</Text>
            <Text>
              {job.scheduled_time_window 
                ? `${job.scheduled_time_window.start} - ${job.scheduled_time_window.end}`
                : 'Not specified'}
            </Text>
          </View>
          
          {job.estimated_arrival_time && (
            <View style={styles.detailRow}>
              <Text style={styles.label}>Estimated Arrival:</Text>
              <Text>{job.estimated_arrival_time}</Text>
            </View>
          )}
          
          <View style={styles.detailRow}>
            <Text style={styles.label}>Estimated Duration:</Text>
            <Text>{job.estimated_duration || 60} minutes</Text>
          </View>
          
          {job.actual_start_time && (
            <View style={styles.detailRow}>
              <Text style={styles.label}>Started At:</Text>
              <Text>{new Date(job.actual_start_time).toLocaleTimeString()}</Text>
            </View>
          )}
          
          {job.actual_end_time && (
            <View style={styles.detailRow}>
              <Text style={styles.label}>Completed At:</Text>
              <Text>{new Date(job.actual_end_time).toLocaleTimeString()}</Text>
            </View>
          )}
          
          {job.notes && (
            <>
              <Divider style={styles.divider} />
              <Text style={styles.label}>Notes:</Text>
              <Paragraph style={styles.notes}>{job.notes}</Paragraph>
            </>
          )}
        </Card.Content>
      </Card>
      
      {/* Customer Information Card */}
      {customer && (
        <Card style={styles.card}>
          <Card.Content>
            <Title>Customer Information</Title>
            
            <View style={styles.detailRow}>
              <Text style={styles.label}>Name:</Text>
              <Text>{customer.name}</Text>
            </View>
            
            <View style={styles.detailRow}>
              <Text style={styles.label}>Phone:</Text>
              <View style={styles.contactRow}>
                <Text>{customer.phone}</Text>
                <IconButton 
                  icon="phone" 
                  size={20} 
                  onPress={() => makePhoneCall(customer.phone)}
                  style={styles.contactIcon}
                />
              </View>
            </View>
            
            <View style={styles.detailRow}>
              <Text style={styles.label}>Email:</Text>
              <View style={styles.contactRow}>
                <Text>{customer.email}</Text>
                <IconButton 
                  icon="email" 
                  size={20} 
                  onPress={() => sendEmail(customer.email)}
                  style={styles.contactIcon}
                />
              </View>
            </View>
            
            <View style={styles.detailRow}>
              <Text style={styles.label}>Service Tier:</Text>
              <Text>{customer.service_tier || 'Standard'}</Text>
            </View>
            
            {customer.notes && (
              <>
                <Divider style={styles.divider} />
                <Text style={styles.label}>Customer Notes:</Text>
                <Paragraph style={styles.notes}>{customer.notes}</Paragraph>
              </>
            )}
          </Card.Content>
        </Card>
      )}
      
      {/* Location Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title>Location</Title>
          
          <View style={styles.detailRow}>
            <Text style={styles.label}>Address:</Text>
            <Text>{job.location?.address || 'No address provided'}</Text>
          </View>
          
          {job.location?.building_info && (
            <View style={styles.detailRow}>
              <Text style={styles.label}>Building Info:</Text>
              <Text>{job.location.building_info}</Text>
            </View>
          )}
          
          {job.location?.access_code && (
            <View style={styles.detailRow}>
              <Text style={styles.label}>Access Code:</Text>
              <Text>{job.location.access_code}</Text>
            </View>
          )}
        </Card.Content>
        
        <Card.Actions>
          <Button 
            mode="contained" 
            icon="navigation" 
            onPress={openMapsNavigation}
          >
            Navigate
          </Button>
        </Card.Actions>
      </Card>
      
      {/* Action Buttons */}
      <View style={styles.actionContainer}>
        {job.status === 'assigned' && (
          <Button 
            mode="contained" 
            icon="play" 
            onPress={handleStartJob}
            style={styles.actionButton}
          >
            Start Job
          </Button>
        )}
        
        {job.status === 'in_progress' && (
          <Button 
            mode="contained" 
            icon="check" 
            onPress={() => setDialogVisible(true)}
            style={styles.actionButton}
          >
            Complete Job
          </Button>
        )}
        
        <Button 
          mode="outlined" 
          icon="crosshairs-gps" 
          onPress={updateLocation}
          style={styles.actionButton}
        >
          Update My Location
        </Button>
      </View>
      
      {/* Completion Dialog */}
      <Portal>
        <Dialog visible={dialogVisible} onDismiss={() => setDialogVisible(false)}>
          <Dialog.Title>Complete Job</Dialog.Title>
          <Dialog.Content>
            <Paragraph>Add any notes about the completed job:</Paragraph>
            <TextInput
              multiline
              numberOfLines={4}
              value={completionNotes}
              onChangeText={setCompletionNotes}
              style={styles.notesInput}
              placeholder="Enter completion notes (optional)"
            />
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setDialogVisible(false)}>Cancel</Button>
            <Button onPress={handleCompleteJob}>Complete</Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 16,
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  statusChip: {
    height: 28,
  },
  serviceType: {
    fontWeight: 'bold',
    fontSize: 16,
    marginBottom: 8,
  },
  divider: {
    marginVertical: 12,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  contactRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  contactIcon: {
    margin: 0,
    marginLeft: 4,
  },
  label: {
    fontWeight: 'bold',
  },
  notes: {
    marginTop: 4,
    fontStyle: 'italic',
  },
  actionContainer: {
    marginBottom: 24,
  },
  actionButton: {
    marginBottom: 12,
  },
  notesInput: {
    marginTop: 8,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  errorText: {
    fontSize: 16,
    color: '#F44336',
    marginBottom: 16,
    textAlign: 'center',
  },
});

export default JobDetailScreen;
