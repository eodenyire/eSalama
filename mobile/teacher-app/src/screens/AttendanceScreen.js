/**
 * Attendance Screen for Teacher App
 */
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, RefreshControl, TouchableOpacity, Alert } from 'react-native';
import AuthService from '../services/auth.service';
import { ENDPOINTS } from '../config/api';

const AttendanceScreen = () => {
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [dateFilter, setDateFilter] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    loadAttendance();
  }, [dateFilter]);

  const loadAttendance = async () => {
    try {
      const api = AuthService.getAxiosInstance();
      const response = await api.get(`${ENDPOINTS.ATTENDANCE}?date=${dateFilter}`);
      setAttendance(response.data);
    } catch (error) {
      console.error('Error loading attendance:', error);
      Alert.alert('Error', 'Failed to load attendance');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadAttendance();
  };

  const renderAttendanceItem = ({ item }) => (
    <View style={styles.attendanceCard}>
      <View style={styles.attendanceHeader}>
        <Text style={styles.studentName}>{item.student?.full_name || 'Unknown Student'}</Text>
        <View style={[styles.typeBadge, item.type === 'arrival' ? styles.arrivalBadge : styles.departureBadge]}>
          <Text style={styles.typeText}>{item.type?.toUpperCase()}</Text>
        </View>
      </View>
      <Text style={styles.attendanceTime}>Time: {new Date(item.timestamp).toLocaleTimeString()}</Text>
      {item.latitude && <Text style={styles.attendanceLocation}>Location: {item.latitude.toFixed(4)}, {item.longitude.toFixed(4)}</Text>}
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Class Attendance</Text>
        <Text style={styles.subtitle}>{new Date(dateFilter).toLocaleDateString()}</Text>
      </View>

      <FlatList
        data={attendance}
        renderItem={renderAttendanceItem}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#FF9800']} />}
        ListEmptyComponent={<Text style={styles.emptyText}>No attendance records for today</Text>}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { backgroundColor: '#FF9800', padding: 20, paddingTop: 50 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#fff' },
  subtitle: { fontSize: 14, color: '#fff', marginTop: 5 },
  listContainer: { padding: 15 },
  attendanceCard: { backgroundColor: '#fff', borderRadius: 8, padding: 15, marginBottom: 10, elevation: 2 },
  attendanceHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  studentName: { fontSize: 16, fontWeight: 'bold', color: '#333' },
  typeBadge: { paddingHorizontal: 10, paddingVertical: 5, borderRadius: 5 },
  arrivalBadge: { backgroundColor: '#4CAF50' },
  departureBadge: { backgroundColor: '#f44336' },
  typeText: { fontSize: 10, fontWeight: 'bold', color: '#fff' },
  attendanceTime: { fontSize: 14, color: '#666', marginBottom: 4 },
  attendanceLocation: { fontSize: 12, color: '#999' },
  emptyText: { textAlign: 'center', marginTop: 50, color: '#999', fontSize: 16 },
});

export default AttendanceScreen;
