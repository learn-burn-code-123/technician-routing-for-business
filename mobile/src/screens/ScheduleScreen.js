import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { 
  Text, 
  Card, 
  Title, 
  Paragraph, 
  ActivityIndicator, 
  Button,
  Chip,
  Divider
} from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import api from '../services/api';

const ScheduleScreen = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [schedule, setSchedule] = useState({});
  const [selectedDate, setSelectedDate] = useState(new Date());
  const navigation = useNavigation();
  
  // Status colors for visual indication
  const statusColors = {
    pending: '#FFC107',
    assigned: '#2196F3',
    in_progress: '#FF9800',
    completed: '#4CAF50',
    cancelled: '#F44336'
  };

  // Load schedule data when component mounts or date changes
  useEffect(() => {
    fetchSchedule();
  }, [selectedDate]);

  // Fetch schedule data from API
  const fetchSchedule = async () => {
    try {
      setError(null);
      setLoading(true);
      
      // Get date range (7 days)
      const dates = getDateRange();
      
      // Create empty schedule object
      const newSchedule = {};
      
      // Initialize each date in the schedule
      dates.forEach(date => {
        newSchedule[formatDate(date)] = [];
      });
      
      // Get jobs for date range
      const startDate = formatDate(dates[0]);
      const endDate = formatDate(dates[dates.length - 1]);
      
      const response = await api.get('/jobs', { 
        params: { 
          start_date: startDate,
          end_date: endDate
        } 
      });
      
      // Group jobs by date
      response.data.forEach(job => {
        const jobDate = job.scheduled_date;
        if (newSchedule[jobDate]) {
          newSchedule[jobDate].push(job);
        }
      });
      
      setSchedule(newSchedule);
    } catch (err) {
      setError('Failed to load schedule. Please try again.');
      console.error('Error fetching schedule:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Handle pull-to-refresh
  const onRefresh = () => {
    setRefreshing(true);
    fetchSchedule();
  };

  // Get date range (7 days) centered on selected date
  const getDateRange = () => {
    const dates = [];
    const startDate = new Date(selectedDate);
    startDate.setDate(startDate.getDate() - 3);
    
    for (let i = 0; i < 7; i++) {
      const date = new Date(startDate);
      date.setDate(date.getDate() + i);
      dates.push(date);
    }
    
    return dates;
  };

  // Format date to YYYY-MM-DD
  const formatDate = (date) => {
    return date.toISOString().split('T')[0];
  };

  // Format date for display
  const formatDisplayDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    // Check if date is today or tomorrow
    if (formatDate(date) === formatDate(today)) {
      return 'Today';
    } else if (formatDate(date) === formatDate(tomorrow)) {
      return 'Tomorrow';
    } else {
      // Format as day of week + date
      const options = { weekday: 'short', month: 'short', day: 'numeric' };
      return date.toLocaleDateString(undefined, options);
    }
  };

  // Navigate to job details
  const navigateToJobDetails = (jobId) => {
    navigation.navigate('JobDetail', { jobId });
  };

  // Navigate to previous week
  const goToPreviousWeek = () => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() - 7);
    setSelectedDate(newDate);
  };

  // Navigate to next week
  const goToNextWeek = () => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + 7);
    setSelectedDate(newDate);
  };

  // Go to today
  const goToToday = () => {
    setSelectedDate(new Date());
  };

  // Render job item
  const renderJobItem = (job) => {
    return (
      <Card 
        key={job._id} 
        style={styles.jobCard}
        onPress={() => navigateToJobDetails(job._id)}
      >
        <Card.Content>
          <View style={styles.jobHeader}>
            <Title style={styles.jobTitle}>
              {job.service_type}
            </Title>
            <Chip 
              style={[styles.statusChip, { backgroundColor: statusColors[job.status] || '#999' }]}
              textStyle={{ color: '#fff' }}
            >
              {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
            </Chip>
          </View>
          
          <Paragraph>
            <Text style={styles.label}>Time: </Text>
            {job.scheduled_time_window 
              ? `${job.scheduled_time_window.start} - ${job.scheduled_time_window.end}`
              : 'No time specified'}
          </Paragraph>
          
          <Paragraph>
            <Text style={styles.label}>Location: </Text>
            {job.location?.address || 'No address provided'}
          </Paragraph>
          
          {job.estimated_arrival_time && (
            <Paragraph>
              <Text style={styles.label}>ETA: </Text>
              {job.estimated_arrival_time}
            </Paragraph>
          )}
        </Card.Content>
      </Card>
    );
  };

  // Render day schedule
  const renderDaySchedule = (dateString) => {
    const jobs = schedule[dateString] || [];
    const displayDate = formatDisplayDate(dateString);
    
    return (
      <View key={dateString} style={styles.dayContainer}>
        <View style={styles.dateHeader}>
          <Text style={styles.dateText}>{displayDate}</Text>
          <Text style={styles.dateSubtext}>{dateString}</Text>
        </View>
        
        {jobs.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Card.Content>
              <Text style={styles.emptyText}>No jobs scheduled</Text>
            </Card.Content>
          </Card>
        ) : (
          jobs.map(job => renderJobItem(job))
        )}
      </View>
    );
  };

  if (loading && !refreshing) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0066cc" />
        <Text style={styles.loadingText}>Loading schedule...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Navigation buttons */}
      <View style={styles.navigationContainer}>
        <Button 
          mode="outlined" 
          onPress={goToPreviousWeek}
          icon="chevron-left"
        >
          Previous
        </Button>
        
        <Button 
          mode="contained" 
          onPress={goToToday}
        >
          Today
        </Button>
        
        <Button 
          mode="outlined" 
          onPress={goToNextWeek}
          icon="chevron-right"
          contentStyle={{ flexDirection: 'row-reverse' }}
        >
          Next
        </Button>
      </View>
      
      {error ? (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <Button mode="contained" onPress={fetchSchedule}>
            Retry
          </Button>
        </View>
      ) : (
        <ScrollView 
          style={styles.scrollView}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={['#0066cc']}
            />
          }
        >
          {Object.keys(schedule).sort().map(dateString => renderDaySchedule(dateString))}
        </ScrollView>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  navigationContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 16,
    backgroundColor: '#fff',
    elevation: 2,
  },
  scrollView: {
    flex: 1,
  },
  dayContainer: {
    marginBottom: 16,
    paddingHorizontal: 16,
  },
  dateHeader: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginVertical: 8,
  },
  dateText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginRight: 8,
  },
  dateSubtext: {
    fontSize: 14,
    color: '#757575',
  },
  jobCard: {
    marginBottom: 8,
  },
  jobHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  jobTitle: {
    fontSize: 16,
  },
  statusChip: {
    height: 24,
  },
  label: {
    fontWeight: 'bold',
  },
  emptyCard: {
    marginBottom: 8,
    backgroundColor: '#f9f9f9',
  },
  emptyText: {
    textAlign: 'center',
    color: '#757575',
    fontStyle: 'italic',
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

export default ScheduleScreen;
