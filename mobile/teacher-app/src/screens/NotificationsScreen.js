/**
 * Notifications Screen for Teacher App - Send and View Notifications
 */
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet, Alert, ScrollView } from 'react-native';
import AuthService from '../services/auth.service';
import { ENDPOINTS } from '../config/api';

const NotificationsScreen = () => {
  const [notifications, setNotifications] = useState([]);
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    loadStudents();
    loadNotifications();
  }, []);

  const loadStudents = async () => {
    try {
      const api = AuthService.getAxiosInstance();
      const response = await api.get(ENDPOINTS.STUDENTS);
      setStudents(response.data);
    } catch (error) {
      console.error('Error loading students:', error);
    }
  };

  const loadNotifications = async () => {
    try {
      const api = AuthService.getAxiosInstance();
      const response = await api.get(ENDPOINTS.NOTIFICATIONS);
      setNotifications(response.data);
    } catch (error) {
      console.error('Error loading notifications:', error);
    }
  };

  const sendNotification = async () => {
    if (!selectedStudent || !message) {
      Alert.alert('Error', 'Please select a student and enter a message');
      return;
    }

    setSending(true);
    try {
      const api = AuthService.getAxiosInstance();
      await api.post(ENDPOINTS.NOTIFICATIONS, {
        student_id: selectedStudent.id,
        type: 'teacher_message',
        message: message,
      });
      Alert.alert('Success', 'Notification sent to parent');
      setMessage('');
      loadNotifications();
    } catch (error) {
      Alert.alert('Error', 'Failed to send notification');
    } finally {
      setSending(false);
    }
  };

  const renderNotification = ({ item }) => (
    <View style={styles.notificationCard}>
      <Text style={styles.notificationStudent}>{item.student?.full_name || 'Unknown'}</Text>
      <Text style={styles.notificationMessage}>{item.message}</Text>
      <Text style={styles.notificationTime}>{new Date(item.sent_at).toLocaleString()}</Text>
    </View>
  );

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Notifications</Text>
      </View>

      <View style={styles.sendCard}>
        <Text style={styles.cardTitle}>Send Notification to Parent</Text>
        
        <Text style={styles.label}>Select Student</Text>
        <View style={styles.studentList}>
          {students.map((student) => (
            <TouchableOpacity
              key={student.id}
              style={[styles.studentButton, selectedStudent?.id === student.id && styles.selectedStudent]}
              onPress={() => setSelectedStudent(student)}
            >
              <Text style={[styles.studentButtonText, selectedStudent?.id === student.id && styles.selectedStudentText]}>
                {student.full_name}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.label}>Message</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter notification message..."
          value={message}
          onChangeText={setMessage}
          multiline
          numberOfLines={4}
        />

        <TouchableOpacity style={styles.sendButton} onPress={sendNotification} disabled={sending}>
          <Text style={styles.sendButtonText}>{sending ? 'Sending...' : 'Send Notification'}</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.historyCard}>
        <Text style={styles.cardTitle}>Recent Notifications</Text>
        <FlatList
          data={notifications}
          renderItem={renderNotification}
          keyExtractor={(item) => item.id.toString()}
          ListEmptyComponent={<Text style={styles.emptyText}>No notifications sent yet</Text>}
          scrollEnabled={false}
        />
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { backgroundColor: '#FF9800', padding: 20, paddingTop: 50 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#fff' },
  sendCard: { backgroundColor: '#fff', margin: 15, padding: 20, borderRadius: 8, elevation: 2 },
  cardTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 15 },
  label: { fontSize: 14, fontWeight: '500', marginBottom: 10, color: '#666' },
  studentList: { flexDirection: 'row', flexWrap: 'wrap', marginBottom: 15 },
  studentButton: { backgroundColor: '#f0f0f0', padding: 10, borderRadius: 5, margin: 5 },
  selectedStudent: { backgroundColor: '#FF9800' },
  studentButtonText: { fontSize: 12, color: '#666' },
  selectedStudentText: { color: '#fff', fontWeight: 'bold' },
  input: { backgroundColor: '#f9f9f9', borderRadius: 8, padding: 15, marginBottom: 15, borderWidth: 1, borderColor: '#ddd', textAlignVertical: 'top' },
  sendButton: { backgroundColor: '#FF9800', padding: 15, borderRadius: 8, alignItems: 'center' },
  sendButtonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  historyCard: { backgroundColor: '#fff', margin: 15, marginTop: 0, padding: 20, borderRadius: 8, elevation: 2 },
  notificationCard: { padding: 15, borderBottomWidth: 1, borderBottomColor: '#f0f0f0' },
  notificationStudent: { fontSize: 14, fontWeight: 'bold', color: '#333', marginBottom: 5 },
  notificationMessage: { fontSize: 14, color: '#666', marginBottom: 5 },
  notificationTime: { fontSize: 12, color: '#999' },
  emptyText: { textAlign: 'center', marginTop: 20, color: '#999', fontSize: 14 },
});

export default NotificationsScreen;
