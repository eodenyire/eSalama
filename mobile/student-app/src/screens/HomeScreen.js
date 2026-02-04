/**
 * Home Screen for Student App
 * Main dashboard with QR code display and status
 */
import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  ScrollView,
} from 'react-native';
import QRCode from 'react-native-qrcode-svg';
import AuthService from '../services/auth.service';
import QRService from '../services/qr.service';
import LocationService from '../services/location.service';
import { CONFIG } from '../config/api';

const HomeScreen = ({ navigation }) => {
  const [qrData, setQrData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [studentInfo, setStudentInfo] = useState(null);
  const [locationTracking, setLocationTracking] = useState(false);
  const [timeUntilExpiry, setTimeUntilExpiry] = useState(null);
  
  const qrRefreshInterval = useRef(null);
  const expiryCountdown = useRef(null);

  useEffect(() => {
    initializeApp();
    
    return () => {
      // Cleanup
      if (qrRefreshInterval.current) {
        clearInterval(qrRefreshInterval.current);
      }
      if (expiryCountdown.current) {
        clearInterval(expiryCountdown.current);
      }
      LocationService.stopTracking();
    };
  }, []);

  const initializeApp = async () => {
    try {
      const user = AuthService.getUser();
      if (!user) {
        navigation.replace('Login');
        return;
      }

      // For demo, use user ID as student ID
      // In production, fetch actual student record
      const studentId = user.id;
      setStudentInfo({ id: studentId, name: user.full_name });

      // Generate initial QR code
      await refreshQRCode(studentId);

      // Start location tracking
      const trackingStarted = await LocationService.startTracking(studentId);
      setLocationTracking(trackingStarted);

      // Set up auto-refresh for QR code (every minute)
      qrRefreshInterval.current = setInterval(() => {
        refreshQRCode(studentId);
      }, CONFIG.QR_REFRESH_INTERVAL);

      setLoading(false);
    } catch (error) {
      console.error('Error initializing app:', error);
      Alert.alert('Error', 'Failed to initialize app');
      setLoading(false);
    }
  };

  const refreshQRCode = async (studentId) => {
    try {
      const qrCode = await QRService.generateQRCode(studentId, 'arrival');
      setQrData(qrCode);
      
      // Start countdown timer
      startExpiryCountdown(qrCode.expiresAt);
    } catch (error) {
      console.error('Error refreshing QR code:', error);
    }
  };

  const startExpiryCountdown = (expiresAt) => {
    if (expiryCountdown.current) {
      clearInterval(expiryCountdown.current);
    }

    expiryCountdown.current = setInterval(() => {
      const now = new Date();
      const diff = expiresAt - now;
      
      if (diff <= 0) {
        setTimeUntilExpiry('Expired');
        clearInterval(expiryCountdown.current);
      } else {
        const minutes = Math.floor(diff / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);
        setTimeUntilExpiry(`${minutes}:${seconds.toString().padStart(2, '0')}`);
      }
    }, 1000);
  };

  const handleSOSAlert = async () => {
    Alert.alert(
      'SOS Alert',
      'Are you sure you want to send an emergency alert?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Send Alert',
          style: 'destructive',
          onPress: async () => {
            try {
              const api = AuthService.getAxiosInstance();
              await api.post('/api/v1/notifications', {
                student_id: studentInfo.id,
                type: 'sos',
                message: `EMERGENCY: SOS alert from ${studentInfo.name}`,
              });
              Alert.alert('Success', 'Emergency alert sent');
            } catch (error) {
              Alert.alert('Error', 'Failed to send alert');
            }
          },
        },
      ]
    );
  };

  const handleLogout = async () => {
    LocationService.stopTracking();
    await AuthService.logout();
    navigation.replace('Login');
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Initializing...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>eSalama Student</Text>
        <Text style={styles.subtitle}>
          {studentInfo?.name || 'Student'}
        </Text>
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.statusCard}>
        <Text style={styles.statusLabel}>Status:</Text>
        <View style={styles.statusRow}>
          <View style={[styles.statusDot, locationTracking && styles.statusDotActive]} />
          <Text style={styles.statusText}>
            {locationTracking ? 'Location Tracking Active' : 'Location Tracking Inactive'}
          </Text>
        </View>
      </View>

      <View style={styles.qrCard}>
        <Text style={styles.cardTitle}>Your QR Code</Text>
        <Text style={styles.cardSubtitle}>Show this to the gate scanner</Text>
        
        {qrData && qrData.qrCode ? (
          <View style={styles.qrContainer}>
            <QRCode
              value={qrData.qrCode}
              size={250}
              backgroundColor="white"
            />
            <Text style={styles.expiryText}>
              Expires in: {timeUntilExpiry || 'Loading...'}
            </Text>
            <Text style={styles.infoText}>
              Auto-refreshes every minute
            </Text>
          </View>
        ) : (
          <ActivityIndicator size="large" color="#4CAF50" />
        )}
      </View>

      <TouchableOpacity style={styles.sosButton} onPress={handleSOSAlert}>
        <Text style={styles.sosText}>🚨 SOS EMERGENCY</Text>
      </TouchableOpacity>

      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>Features</Text>
        <Text style={styles.infoItem}>✓ GPS tracked every 2 minutes</Text>
        <Text style={styles.infoItem}>✓ Auto-refreshing QR code</Text>
        <Text style={styles.infoItem}>✓ Emergency SOS alerts</Text>
        <Text style={styles.infoItem}>✓ Real-time parent notifications</Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  header: {
    backgroundColor: '#4CAF50',
    padding: 20,
    paddingTop: 50,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 16,
    color: '#fff',
    marginTop: 5,
  },
  logoutButton: {
    marginTop: 10,
    padding: 8,
  },
  logoutText: {
    color: '#fff',
    fontSize: 14,
  },
  statusCard: {
    backgroundColor: '#fff',
    margin: 15,
    padding: 15,
    borderRadius: 8,
    elevation: 2,
  },
  statusLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#ccc',
    marginRight: 10,
  },
  statusDotActive: {
    backgroundColor: '#4CAF50',
  },
  statusText: {
    fontSize: 14,
    color: '#666',
  },
  qrCard: {
    backgroundColor: '#fff',
    margin: 15,
    marginTop: 0,
    padding: 20,
    borderRadius: 8,
    elevation: 2,
    alignItems: 'center',
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  cardSubtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 20,
  },
  qrContainer: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
  },
  expiryText: {
    marginTop: 15,
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FF9800',
  },
  infoText: {
    marginTop: 5,
    fontSize: 12,
    color: '#666',
  },
  sosButton: {
    backgroundColor: '#f44336',
    margin: 15,
    marginTop: 0,
    padding: 20,
    borderRadius: 8,
    elevation: 2,
    alignItems: 'center',
  },
  sosText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  infoCard: {
    backgroundColor: '#fff',
    margin: 15,
    marginTop: 0,
    padding: 15,
    borderRadius: 8,
    elevation: 2,
    marginBottom: 30,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  infoItem: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
});

export default HomeScreen;
