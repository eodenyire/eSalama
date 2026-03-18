/**
 * Profile Screen for Parent App
 */
import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import AuthService from '../services/auth.service';

const ProfileScreen = ({ navigation }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(AuthService.getUser());
  }, []);

  const handleLogout = async () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', style: 'destructive', onPress: async () => {
        await AuthService.logout();
        navigation.replace('Login');
      }},
    ]);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Profile</Text>
      </View>

      <View style={styles.profileCard}>
        <Text style={styles.label}>Name</Text>
        <Text style={styles.value}>{user?.full_name || 'N/A'}</Text>

        <Text style={styles.label}>Email</Text>
        <Text style={styles.value}>{user?.email || 'N/A'}</Text>

        <Text style={styles.label}>Phone</Text>
        <Text style={styles.value}>{user?.phone || 'N/A'}</Text>

        <Text style={styles.label}>Role</Text>
        <Text style={styles.value}>{user?.role || 'parent'}</Text>
      </View>

      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutText}>Logout</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { backgroundColor: '#2196F3', padding: 20, paddingTop: 50 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#fff' },
  profileCard: { backgroundColor: '#fff', margin: 15, padding: 20, borderRadius: 8, elevation: 2 },
  label: { fontSize: 12, color: '#999', marginTop: 15, marginBottom: 5 },
  value: { fontSize: 16, color: '#333', fontWeight: '500' },
  logoutButton: { backgroundColor: '#f44336', margin: 15, padding: 15, borderRadius: 8, alignItems: 'center', elevation: 2 },
  logoutText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
});

export default ProfileScreen;
