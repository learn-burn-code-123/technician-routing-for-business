import React, { useState, useEffect, useContext } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { 
  Avatar, 
  Title, 
  Text, 
  Button, 
  Card, 
  Switch, 
  Divider,
  ActivityIndicator,
  List,
  IconButton
} from 'react-native-paper';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';

const ProfileScreen = () => {
  const { userInfo, logout } = useContext(AuthContext);
  const [technician, setTechnician] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [availableStatus, setAvailableStatus] = useState(true);
  const [locationSharing, setLocationSharing] = useState(true);
  const [stats, setStats] = useState({
    todayJobs: 0,
    completedJobs: 0,
    inProgressJobs: 0,
    pendingJobs: 0
  });

  // Load technician profile when component mounts
  useEffect(() => {
    fetchTechnicianProfile();
  }, []);

  // Fetch technician profile from API
  const fetchTechnicianProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get technician profile
      const response = await api.technician.getTechnicianProfile();
      setTechnician(response.data);
      
      // Set status switch based on technician status
      setAvailableStatus(response.data.status === 'available');
      
      // Get job statistics
      await fetchJobStatistics();
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load profile. Please try again.');
      setLoading(false);
      console.error('Error fetching technician profile:', err);
    }
  };

  // Fetch job statistics
  const fetchJobStatistics = async () => {
    try {
      // Get today's date in YYYY-MM-DD format
      const today = new Date().toISOString().split('T')[0];
      
      // Get jobs for today
      const todayResponse = await api.job.getJobs({ date: today });
      
      // Get completed jobs
      const completedResponse = await api.job.getJobs({ status: 'completed' });
      
      // Get in-progress jobs
      const inProgressResponse = await api.job.getJobs({ status: 'in_progress' });
      
      // Get pending jobs
      const pendingResponse = await api.job.getJobs({ status: 'assigned' });
      
      setStats({
        todayJobs: todayResponse.data.length,
        completedJobs: completedResponse.data.length,
        inProgressJobs: inProgressResponse.data.length,
        pendingJobs: pendingResponse.data.length
      });
    } catch (err) {
      console.error('Error fetching job statistics:', err);
    }
  };

  // Toggle technician availability status
  const toggleAvailability = async () => {
    try {
      const newStatus = availableStatus ? 'off-duty' : 'available';
      
      // Update technician status
      await api.technician.updateStatus(newStatus);
      
      // Update local state
      setAvailableStatus(!availableStatus);
      
      // Show success message
      Alert.alert(
        'Status Updated',
        `You are now ${newStatus === 'available' ? 'available' : 'off-duty'}.`
      );
    } catch (err) {
      Alert.alert('Error', 'Failed to update status. Please try again.');
      console.error('Error updating technician status:', err);
    }
  };

  // Toggle location sharing
  const toggleLocationSharing = () => {
    setLocationSharing(!locationSharing);
    
    // In a real app, this would update a setting in the backend
    Alert.alert(
      'Location Sharing',
      `Location sharing is now ${!locationSharing ? 'enabled' : 'disabled'}.`
    );
  };

  // Handle logout
  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        {
          text: 'Cancel',
          style: 'cancel'
        },
        {
          text: 'Logout',
          onPress: logout
        }
      ]
    );
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0066cc" />
        <Text style={styles.loadingText}>Loading profile...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{error}</Text>
        <Button mode="contained" onPress={fetchTechnicianProfile}>
          Retry
        </Button>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Profile Header */}
      <View style={styles.header}>
        <Avatar.Text 
          size={80} 
          label={technician?.name?.split(' ').map(n => n[0]).join('') || 'T'} 
          backgroundColor="#0066cc"
        />
        <Title style={styles.name}>{technician?.name || 'Technician'}</Title>
        <Text style={styles.role}>ISP Technician</Text>
        
        <View style={styles.statusContainer}>
          <Text style={styles.statusText}>
            {availableStatus ? 'Available' : 'Off-Duty'}
          </Text>
          <Switch
            value={availableStatus}
            onValueChange={toggleAvailability}
            color="#4CAF50"
          />
        </View>
      </View>
      
      {/* Statistics Card */}
      <Card style={styles.card}>
        <Card.Title title="Job Statistics" />
        <Card.Content>
          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{stats.todayJobs}</Text>
              <Text style={styles.statLabel}>Today's Jobs</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{stats.completedJobs}</Text>
              <Text style={styles.statLabel}>Completed</Text>
            </View>
          </View>
          
          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{stats.inProgressJobs}</Text>
              <Text style={styles.statLabel}>In Progress</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{stats.pendingJobs}</Text>
              <Text style={styles.statLabel}>Pending</Text>
            </View>
          </View>
        </Card.Content>
      </Card>
      
      {/* Contact Information Card */}
      <Card style={styles.card}>
        <Card.Title title="Contact Information" />
        <Card.Content>
          <List.Item
            title="Email"
            description={technician?.email || 'Not available'}
            left={props => <List.Icon {...props} icon="email" />}
          />
          <Divider />
          <List.Item
            title="Phone"
            description={technician?.phone || 'Not available'}
            left={props => <List.Icon {...props} icon="phone" />}
          />
        </Card.Content>
      </Card>
      
      {/* Skills Card */}
      <Card style={styles.card}>
        <Card.Title title="Skills & Certifications" />
        <Card.Content>
          <View style={styles.skillsContainer}>
            {technician?.skills?.map((skill, index) => (
              <View key={index} style={styles.skillItem}>
                <IconButton icon="check-circle" size={20} color="#4CAF50" />
                <Text>{skill}</Text>
              </View>
            )) || (
              <Text style={styles.noDataText}>No skills listed</Text>
            )}
          </View>
        </Card.Content>
      </Card>
      
      {/* Settings Card */}
      <Card style={styles.card}>
        <Card.Title title="Settings" />
        <Card.Content>
          <View style={styles.settingItem}>
            <Text>Location Sharing</Text>
            <Switch
              value={locationSharing}
              onValueChange={toggleLocationSharing}
              color="#0066cc"
            />
          </View>
          <Divider style={styles.divider} />
          <View style={styles.settingItem}>
            <Text>Push Notifications</Text>
            <Switch
              value={true}
              color="#0066cc"
            />
          </View>
        </Card.Content>
      </Card>
      
      {/* Logout Button */}
      <Button 
        mode="outlined" 
        icon="logout" 
        onPress={handleLogout}
        style={styles.logoutButton}
      >
        Logout
      </Button>
      
      {/* App Version */}
      <Text style={styles.versionText}>Version 1.0.0</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',
    marginBottom: 16,
  },
  name: {
    marginTop: 16,
    fontSize: 24,
  },
  role: {
    fontSize: 16,
    color: '#757575',
    marginBottom: 8,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  statusText: {
    marginRight: 8,
    fontWeight: 'bold',
  },
  card: {
    marginHorizontal: 16,
    marginBottom: 16,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#0066cc',
  },
  statLabel: {
    fontSize: 14,
    color: '#757575',
  },
  divider: {
    marginVertical: 8,
  },
  skillsContainer: {
    marginTop: 8,
  },
  skillItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  logoutButton: {
    margin: 16,
  },
  versionText: {
    textAlign: 'center',
    color: '#757575',
    marginBottom: 24,
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
  noDataText: {
    fontStyle: 'italic',
    color: '#757575',
  },
});

export default ProfileScreen;
