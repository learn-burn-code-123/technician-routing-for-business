import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { 
  Card, 
  Title, 
  Paragraph, 
  Chip, 
  ActivityIndicator, 
  Text,
  Button,
  Searchbar,
  Menu,
  Divider
} from 'react-native-paper';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import api from '../services/api';

const JobsScreen = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterMenuVisible, setFilterMenuVisible] = useState(false);
  const [statusFilter, setStatusFilter] = useState('all');
  
  const navigation = useNavigation();

  // Status colors for visual indication
  const statusColors = {
    pending: '#FFC107',
    assigned: '#2196F3',
    in_progress: '#FF9800',
    completed: '#4CAF50',
    cancelled: '#F44336'
  };

  // Load jobs when screen is focused
  useFocusEffect(
    useCallback(() => {
      fetchJobs();
    }, [statusFilter])
  );

  // Fetch jobs from API
  const fetchJobs = async () => {
    try {
      setError(null);
      setLoading(true);
      
      // Prepare filter parameters
      const params = {};
      if (statusFilter !== 'all') {
        params.status = statusFilter;
      }
      
      const response = await api.job.getJobs(params);
      setJobs(response.data);
    } catch (err) {
      setError('Failed to load jobs. Please try again.');
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Handle pull-to-refresh
  const onRefresh = () => {
    setRefreshing(true);
    fetchJobs();
  };

  // Filter jobs based on search query
  const filteredJobs = jobs.filter(job => {
    const searchLower = searchQuery.toLowerCase();
    return (
      job.service_type.toLowerCase().includes(searchLower) ||
      job._id.toLowerCase().includes(searchLower) ||
      (job.location?.address && job.location.address.toLowerCase().includes(searchLower))
    );
  });

  // Navigate to job details
  const handleJobPress = (jobId) => {
    navigation.navigate('JobDetail', { jobId });
  };

  // Render job status chip
  const renderStatusChip = (status) => {
    return (
      <Chip 
        style={[styles.statusChip, { backgroundColor: statusColors[status] || '#999' }]}
        textStyle={{ color: '#fff' }}
      >
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Chip>
    );
  };

  // Render job item
  const renderJobItem = ({ item }) => {
    // Format scheduled time window
    const timeWindow = item.scheduled_time_window 
      ? `${item.scheduled_time_window.start} - ${item.scheduled_time_window.end}`
      : 'No time specified';

    return (
      <Card style={styles.card} onPress={() => handleJobPress(item._id)}>
        <Card.Content>
          <View style={styles.cardHeader}>
            <Title>Job #{item._id.substring(0, 8)}</Title>
            {renderStatusChip(item.status)}
          </View>
          
          <Paragraph style={styles.serviceType}>
            {item.service_type.toUpperCase()}
          </Paragraph>
          
          <Paragraph>
            <Text style={styles.label}>Location: </Text>
            {item.location?.address || 'No address provided'}
          </Paragraph>
          
          <Paragraph>
            <Text style={styles.label}>Date: </Text>
            {item.scheduled_date}
          </Paragraph>
          
          <Paragraph>
            <Text style={styles.label}>Time: </Text>
            {timeWindow}
          </Paragraph>
          
          {item.estimated_arrival_time && (
            <Paragraph>
              <Text style={styles.label}>ETA: </Text>
              {item.estimated_arrival_time}
            </Paragraph>
          )}
        </Card.Content>
        
        <Card.Actions>
          <Button 
            mode="contained" 
            onPress={() => handleJobPress(item._id)}
          >
            View Details
          </Button>
          
          {item.status === 'assigned' && (
            <Button 
              mode="outlined" 
              onPress={() => startJob(item._id)}
              style={{ marginLeft: 8 }}
            >
              Start Job
            </Button>
          )}
        </Card.Actions>
      </Card>
    );
  };

  // Start a job
  const startJob = async (jobId) => {
    try {
      await api.job.startJob(jobId);
      fetchJobs(); // Refresh job list
    } catch (err) {
      console.error('Error starting job:', err);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Searchbar
          placeholder="Search jobs..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchbar}
        />
        
        <Menu
          visible={filterMenuVisible}
          onDismiss={() => setFilterMenuVisible(false)}
          anchor={
            <Button 
              mode="outlined" 
              onPress={() => setFilterMenuVisible(true)}
              icon="filter-variant"
            >
              Filter
            </Button>
          }
        >
          <Menu.Item 
            onPress={() => {
              setStatusFilter('all');
              setFilterMenuVisible(false);
            }} 
            title="All Jobs" 
          />
          <Divider />
          <Menu.Item 
            onPress={() => {
              setStatusFilter('assigned');
              setFilterMenuVisible(false);
            }} 
            title="Assigned" 
          />
          <Menu.Item 
            onPress={() => {
              setStatusFilter('in_progress');
              setFilterMenuVisible(false);
            }} 
            title="In Progress" 
          />
          <Menu.Item 
            onPress={() => {
              setStatusFilter('completed');
              setFilterMenuVisible(false);
            }} 
            title="Completed" 
          />
        </Menu>
      </View>
      
      {loading && !refreshing ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#0066cc" />
          <Text style={styles.loadingText}>Loading jobs...</Text>
        </View>
      ) : error ? (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <Button mode="contained" onPress={fetchJobs}>
            Retry
          </Button>
        </View>
      ) : filteredJobs.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>No jobs found</Text>
          <Text style={styles.emptySubtext}>
            {searchQuery 
              ? 'Try a different search term' 
              : statusFilter !== 'all' 
                ? `No ${statusFilter} jobs found` 
                : 'You have no assigned jobs at the moment'}
          </Text>
          <Button mode="contained" onPress={fetchJobs} style={styles.retryButton}>
            Refresh
          </Button>
        </View>
      ) : (
        <FlatList
          data={filteredJobs}
          renderItem={renderJobItem}
          keyExtractor={item => item._id}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={['#0066cc']}
            />
          }
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  searchContainer: {
    flexDirection: 'row',
    padding: 16,
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  searchbar: {
    flex: 1,
    marginRight: 8,
  },
  listContent: {
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
    marginBottom: 8,
  },
  label: {
    fontWeight: 'bold',
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
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#757575',
    textAlign: 'center',
    marginBottom: 16,
  },
  retryButton: {
    marginTop: 16,
  },
});

export default JobsScreen;
