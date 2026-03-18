/**
 * Location Tracking Service
 * Tracks GPS location every 2 minutes and sends to backend
 */
import Geolocation from 'react-native-geolocation-service';
import { Platform, PermissionsAndroid } from 'react-native';
import AuthService from './auth.service';
import { ENDPOINTS, CONFIG } from '../config/api';

class LocationService {
  constructor() {
    this.watchId = null;
    this.interval = null;
    this.studentId = null;
  }

  /**
   * Request location permissions
   */
  async requestPermissions() {
    if (Platform.OS === 'android') {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
        {
          title: 'eSalama Location Permission',
          message: 'eSalama needs access to your location for tracking',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'OK',
        }
      );
      return granted === PermissionsAndroid.RESULTS.GRANTED;
    }
    return true;
  }

  /**
   * Get current location
   */
  getCurrentLocation() {
    return new Promise((resolve, reject) => {
      Geolocation.getCurrentPosition(
        position => {
          const { latitude, longitude, accuracy } = position.coords;
          resolve({ latitude, longitude, accuracy });
        },
        error => {
          console.error('Location error:', error);
          reject(error);
        },
        {
          enableHighAccuracy: true,
          timeout: 15000,
          maximumAge: 10000,
        }
      );
    });
  }

  /**
   * Send location to backend
   */
  async sendLocation(latitude, longitude, accuracy) {
    try {
      if (!this.studentId) {
        console.error('No student ID set for location tracking');
        return;
      }

      const api = AuthService.getAxiosInstance();
      await api.post(ENDPOINTS.LOCATION, {
        student_id: this.studentId,
        latitude,
        longitude,
        accuracy,
        timestamp: new Date().toISOString(),
      });

      console.log('Location sent successfully:', { latitude, longitude, accuracy });
    } catch (error) {
      console.error('Error sending location:', error);
    }
  }

  /**
   * Start tracking location
   */
  async startTracking(studentId) {
    this.studentId = studentId;

    // Check permissions
    const hasPermission = await this.requestPermissions();
    if (!hasPermission) {
      console.error('Location permission denied');
      return false;
    }

    // Send initial location
    try {
      const location = await this.getCurrentLocation();
      await this.sendLocation(location.latitude, location.longitude, location.accuracy);
    } catch (error) {
      console.error('Error getting initial location:', error);
    }

    // Set up periodic location tracking (every 2 minutes)
    this.interval = setInterval(async () => {
      try {
        const location = await this.getCurrentLocation();
        await this.sendLocation(location.latitude, location.longitude, location.accuracy);
      } catch (error) {
        console.error('Error in periodic location tracking:', error);
      }
    }, CONFIG.LOCATION_INTERVAL);

    console.log('Location tracking started');
    return true;
  }

  /**
   * Stop tracking location
   */
  stopTracking() {
    if (this.watchId) {
      Geolocation.clearWatch(this.watchId);
      this.watchId = null;
    }

    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }

    console.log('Location tracking stopped');
  }
}

export default new LocationService();
