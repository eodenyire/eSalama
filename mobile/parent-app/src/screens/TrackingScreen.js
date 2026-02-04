/**
 * Tracking Screen for Parent App - Real-time GPS Tracking
 */
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, TouchableOpacity, ActivityIndicator } from 'react-native';
import MapView, { Marker, Polyline } from 'react-native-maps';
import AuthService from '../services/auth.service';
import { ENDPOINTS } from '../config/api';

const TrackingScreen = () => {
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [lastLocation, setLastLocation] = useState(null);
  const [locationHistory, setLocationHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStudents();
  }, []);

  useEffect(() => {
    if (selectedStudent) {
      loadLocationData();
      const interval = setInterval(loadLocationData, 30000); // Refresh every 30 seconds
      return () => clearInterval(interval);
    }
  }, [selectedStudent]);

  const loadStudents = async () => {
    try {
      const api = AuthService.getAxiosInstance();
      const response = await api.get(ENDPOINTS.STUDENTS);
      setStudents(response.data);
      if (response.data.length > 0) {
        setSelectedStudent(response.data[0]);
      }
    } catch (error) {
      console.error('Error loading students:', error);
      Alert.alert('Error', 'Failed to load students');
    } finally {
      setLoading(false);
    }
  };

  const loadLocationData = async () => {
    if (!selectedStudent) return;
    try {
      const api = AuthService.getAxiosInstance();
      const [lastLoc, history] = await Promise.all([
        api.get(ENDPOINTS.LOCATION_LAST(selectedStudent.id)),
        api.get(ENDPOINTS.LOCATION_HISTORY(selectedStudent.id) + '?limit=50'),
      ]);
      setLastLocation(lastLoc.data);
      setLocationHistory(history.data);
    } catch (error) {
      console.error('Error loading location:', error);
    }
  };

  if (loading) {
    return <View style={styles.loadingContainer}><ActivityIndicator size="large" color="#2196F3" /></View>;
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Live Tracking</Text>
        {selectedStudent && <Text style={styles.subtitle}>{selectedStudent.full_name}</Text>}
      </View>

      {lastLocation ? (
        <MapView
          style={styles.map}
          initialRegion={{
            latitude: lastLocation.latitude,
            longitude: lastLocation.longitude,
            latitudeDelta: 0.01,
            longitudeDelta: 0.01,
          }}
        >
          <Marker coordinate={{ latitude: lastLocation.latitude, longitude: lastLocation.longitude }} title={selectedStudent?.full_name} description={`Last updated: ${new Date(lastLocation.timestamp).toLocaleTimeString()}`} pinColor="#2196F3" />
          {locationHistory.length > 1 && <Polyline coordinates={locationHistory.map(loc => ({ latitude: loc.latitude, longitude: loc.longitude }))} strokeColor="#2196F3" strokeWidth={3} />}
        </MapView>
      ) : (
        <View style={styles.noLocationContainer}>
          <Text style={styles.noLocationText}>No location data available</Text>
        </View>
      )}

      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>Location Info</Text>
        {lastLocation && (
          <>
            <Text style={styles.infoText}>Accuracy: ±{lastLocation.accuracy?.toFixed(0) || 'N/A'}m</Text>
            <Text style={styles.infoText}>Last Update: {new Date(lastLocation.timestamp).toLocaleString()}</Text>
          </>
        )}
        <TouchableOpacity style={styles.refreshButton} onPress={loadLocationData}>
          <Text style={styles.refreshButtonText}>Refresh Location</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  header: { backgroundColor: '#2196F3', padding: 20, paddingTop: 50 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#fff' },
  subtitle: { fontSize: 14, color: '#fff', marginTop: 5 },
  map: { flex: 1 },
  noLocationContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  noLocationText: { fontSize: 16, color: '#999' },
  infoCard: { backgroundColor: '#fff', padding: 15, borderTopLeftRadius: 15, borderTopRightRadius: 15, elevation: 5 },
  infoTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  infoText: { fontSize: 14, color: '#666', marginBottom: 5 },
  refreshButton: { marginTop: 10, backgroundColor: '#2196F3', padding: 12, borderRadius: 8, alignItems: 'center' },
  refreshButtonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
});

export default TrackingScreen;
