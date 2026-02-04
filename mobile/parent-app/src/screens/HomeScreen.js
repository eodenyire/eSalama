/**
 * Home Screen for Parent App - Notifications Dashboard
 */
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, RefreshControl, Alert } from 'react-native';
import AuthService from '../services/auth.service';
import { ENDPOINTS } from '../config/api';

const HomeScreen = ({ navigation }) => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(AuthService.getUser());
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      const api = AuthService.getAxiosInstance();
      const response = await api.get(ENDPOINTS.NOTIFICATIONS);
      setNotifications(response.data);
    } catch (error) {
      console.error('Error loading notifications:', error);
      Alert.alert('Error', 'Failed to load notifications');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadNotifications();
  };

  const markAsRead = async (notificationId) => {
    try {
      const api = AuthService.getAxiosInstance();
      await api.put(ENDPOINTS.NOTIFICATION_READ(notificationId));
      loadNotifications();
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const renderNotification = ({ item }) => (
    <TouchableOpacity style={[styles.notificationCard, !item.is_read && styles.unreadCard]} onPress={() => markAsRead(item.id)}>
      <View style={styles.notificationHeader}>
        <Text style={styles.notificationType}>{item.type?.toUpperCase() || 'NOTIFICATION'}</Text>
        <Text style={styles.notificationTime}>{new Date(item.sent_at).toLocaleTimeString()}</Text>
      </View>
      <Text style={styles.notificationMessage}>{item.message}</Text>
      {!item.is_read && <View style={styles.unreadDot} />}
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Notifications</Text>
        <Text style={styles.subtitle}>Hello, {user?.full_name || 'Parent'}!</Text>
      </View>

      <FlatList
        data={notifications}
        renderItem={renderNotification}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#2196F3']} />}
        ListEmptyComponent={<Text style={styles.emptyText}>No notifications</Text>}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { backgroundColor: '#2196F3', padding: 20, paddingTop: 50 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#fff' },
  subtitle: { fontSize: 14, color: '#fff', marginTop: 5 },
  listContainer: { padding: 15 },
  notificationCard: { backgroundColor: '#fff', borderRadius: 8, padding: 15, marginBottom: 10, elevation: 2 },
  unreadCard: { borderLeftWidth: 4, borderLeftColor: '#2196F3' },
  notificationHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  notificationType: { fontSize: 12, fontWeight: 'bold', color: '#2196F3' },
  notificationTime: { fontSize: 12, color: '#999' },
  notificationMessage: { fontSize: 14, color: '#333' },
  unreadDot: { position: 'absolute', top: 10, right: 10, width: 8, height: 8, borderRadius: 4, backgroundColor: '#2196F3' },
  emptyText: { textAlign: 'center', marginTop: 50, color: '#999', fontSize: 16 },
});

export default HomeScreen;
