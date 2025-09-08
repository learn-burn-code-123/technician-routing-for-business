import React, { useState, useEffect, useRef } from 'react';
import { View, StyleSheet, Dimensions, Alert } from 'react-native';
import { ActivityIndicator, Text, FAB, Card, Title, Paragraph, Button } from 'react-native-paper';
import MapView, { Marker, Callout, PROVIDER_GOOGLE } from 'react-native-maps';
import * as Location from 'expo-location';
import { useNavigation } from '@react-navigation/native';
import api from '../services/api';

const MapScreen = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentLocation, setCurrentLocation] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const mapRef = useRef(null);
  const navigation = useNavigation();

  // Status colors for map markers
  const statusColors = {
    pending: '#FFC107',
    assigned: '#2196F3',
    in_progress: '#FF9800',
    completed: '#4CAF50',
    cancelled: '#F44336'
  };

  // Load initial data when screen mounts
  useEffect(() => {
    loadInitialData();
  }, []);

  // Load current location and job data
  const loadInitialData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get current location
      await getCurrentLocation();
      
      // Get jobs
      await fetchJobs();
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load map data. Please try again.');
      setLoading(false);
      console.error('Error loading map data:', err);
    }
  };

  // Get current location
  const getCurrentLocation = async () => {
    try {
      // Request location permission
      const { status } = await Location.requestForegroundPermissionsAsync();
      
      if (status !== 'granted') {
        setError('Location permission is required to show your position on the map.');
        return;
      }
      
      // Get current location
      const location = await Location.getCurrentPositionAsync({});
      const { latitude, longitude } = location.coords;
      
      setCurrentLocation({
        latitude,
        longitude,
        latitudeDelta: 0.05,
        longitudeDelta: 0.05
      });
      
      // Update technician location in the backend
      await api.technician.updateLocation({
        lat: latitude,
        lng: longitude
      });
      
    } catch (err) {
      console.error('Error getting current location:', err);
      setError('Failed to get your current location.');
    }
  };

  // Fetch jobs from API
  const fetchJobs = async () => {
    try {
      // Get today's date in YYYY-MM-DD format
      const today = new Date().toISOString().split('T')[0];
      
      // Get jobs for today
      const response = await api.job.getJobs({ date: today });
      
      // Filter jobs with valid location data
      const jobsWithLocation = response.data.filter(job => 
        job.location && job.location.lat && job.location.lng
      );
      
      setJobs(jobsWithLocation);
    } catch (err) {
      console.error('Error fetching jobs:', err);
      setError('Failed to load job data.');
    }
  };

  // Refresh map data
  const refreshMapData = async () => {
    try {
      setLoading(true);
      await getCurrentLocation();
      await fetchJobs();
      setLoading(false);
    } catch (err) {
      setLoading(false);
      Alert.alert('Error', 'Failed to refresh map data.');
      console.error('Error refreshing map data:', err);
    }
  };

  // Center map on current location
  const centerOnLocation = () => {
    if (currentLocation && mapRef.current) {
      mapRef.current.animateToRegion(currentLocation, 500);
    } else {
      Alert.alert('Error', 'Current location not available.');
    }
  };

  // Show all jobs on map
  const showAllJobs = () => {
    if (jobs.length === 0 || !mapRef.current) {
      return;
    }
    
    // Calculate bounds that include all jobs and current location
    const points = jobs.map(job => ({
      latitude: job.location.lat,
      longitude: job.location.lng
    }));
    
    if (currentLocation) {
      points.push({
        latitude: currentLocation.latitude,
        longitude: currentLocation.longitude
      });
    }
    
    // Calculate the region that fits all points
    const minLat = Math.min(...points.map(p => p.latitude));
    const maxLat = Math.max(...points.map(p => p.latitude));
    const minLng = Math.min(...points.map(p => p.longitude));
    const maxLng = Math.max(...points.map(p => p.longitude));
    
    const region = {
      latitude: (minLat + maxLat) / 2,
      longitude: (minLng + maxLng) / 2,
      latitudeDelta: (maxLat - minLat) * 1.5,
      longitudeDelta: (maxLng - minLng) * 1.5
    };
    
    mapRef.current.animateToRegion(region, 500);
  };

  // Navigate to job details
  const navigateToJobDetails = (jobId) => {
    navigation.navigate('JobDetail', { jobId });
  };

  if (loading && !currentLocation) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0066cc" />
        <Text style={styles.loadingText}>Loading map...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {error ? (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <Button mode="contained" onPress={loadInitialData}>
            Retry
          </Button>
        </View>
      ) : (
        <>
          <MapView
            ref={mapRef}
            style={styles.map}
            provider={PROVIDER_GOOGLE}
            initialRegion={currentLocation || {
              latitude: 37.78825,
              longitude: -122.4324,
              latitudeDelta: 0.0922,
              longitudeDelta: 0.0421
            }}
            showsUserLocation
            showsMyLocationButton={false}
            onPress={() => setSelectedJob(null)}
          >
            {/* Job markers */}
            {jobs.map(job => (
              <Marker
                key={job._id}
                coordinate={{
                  latitude: job.location.lat,
                  longitude: job.location.lng
                }}
                pinColor={statusColors[job.status] || '#999'}
                onPress={() => setSelectedJob(job)}
              >
                <Callout tooltip>
                  <Card style={styles.calloutCard}>
                    <Card.Content>
                      <Title style={styles.calloutTitle}>
                        {job.service_type}
                      </Title>
                      <Paragraph>
                        {job.location.address}
                      </Paragraph>
                      <Paragraph>
                        Status: {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                      </Paragraph>
                      <Paragraph>
                        Time: {job.scheduled_time_window?.start} - {job.scheduled_time_window?.end}
                      </Paragraph>
                    </Card.Content>
                  </Card>
                </Callout>
              </Marker>
            ))}
          </MapView>
          
          {/* Selected job card */}
          {selectedJob && (
            <Card style={styles.selectedJobCard}>
              <Card.Content>
                <Title>{selectedJob.service_type}</Title>
                <Paragraph>
                  <Text style={styles.label}>Address: </Text>
                  {selectedJob.location.address}
                </Paragraph>
                <Paragraph>
                  <Text style={styles.label}>Status: </Text>
                  {selectedJob.status.charAt(0).toUpperCase() + selectedJob.status.slice(1)}
                </Paragraph>
                <Paragraph>
                  <Text style={styles.label}>Time: </Text>
                  {selectedJob.scheduled_time_window?.start} - {selectedJob.scheduled_time_window?.end}
                </Paragraph>
              </Card.Content>
              <Card.Actions>
                <Button 
                  mode="contained" 
                  onPress={() => navigateToJobDetails(selectedJob._id)}
                >
                  View Details
                </Button>
              </Card.Actions>
            </Card>
          )}
          
          {/* FAB buttons */}
          <FAB
            style={styles.fabRefresh}
            icon="refresh"
            onPress={refreshMapData}
          />
          
          <FAB
            style={styles.fabLocation}
            icon="crosshairs-gps"
            onPress={centerOnLocation}
          />
          
          <FAB
            style={styles.fabShowAll}
            icon="map-marker-multiple"
            onPress={showAllJobs}
          />
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  map: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },
  calloutCard: {
    width: 200,
    borderRadius: 8,
  },
  calloutTitle: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  selectedJobCard: {
    position: 'absolute',
    bottom: 16,
    left: 16,
    right: 16,
    elevation: 4,
  },
  label: {
    fontWeight: 'bold',
  },
  fabRefresh: {
    position: 'absolute',
    margin: 16,
    right: 16,
    top: 16,
    backgroundColor: '#ffffff',
  },
  fabLocation: {
    position: 'absolute',
    margin: 16,
    right: 16,
    bottom: 160,
    backgroundColor: '#ffffff',
  },
  fabShowAll: {
    position: 'absolute',
    margin: 16,
    right: 16,
    bottom: 96,
    backgroundColor: '#ffffff',
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

export default MapScreen;
